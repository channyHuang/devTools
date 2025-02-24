import torch
import torch.nn.functional as F
from einops import rearrange, repeat
from torch import nn
from datetime import datetime

MIN_NUM_PATCHES = 16

# 修改后的ViT网络

class Residual(nn.Module):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn
    def forward(self, x, **kwargs):
        return self.fn(x, **kwargs) + x

class PreNorm(nn.Module):
    def __init__(self, dim, fn):
        super().__init__()
        self.norm = nn.LayerNorm(dim)
        self.fn = fn
    def forward(self, x, **kwargs):
        return self.fn(self.norm(x), **kwargs)

class FeedForward(nn.Module):
    def __init__(self, dim, hidden_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, dim),
            # nn.ReLU(inplace=True)
           
        )
    def forward(self, x):
        return self.net(x)

class Attention(nn.Module):
    def __init__(self, dim, heads = 8):
        super().__init__()
        self.heads = heads
        self.scale = dim ** -0.5

        self.to_qkv = nn.Linear(dim, dim * 3, bias = False)
        self.to_out = nn.Sequential(
            nn.Linear(dim, dim),
           
        )

    def forward(self, x, mask = None):
        b, n, _, h = *x.shape, self.heads
        qkv = self.to_qkv(x).chunk(3, dim = -1)
        q, k, v = map(lambda t: rearrange(t, 'b n (h d) -> b h n d', h = h), qkv)

        dots = torch.einsum('bhid,bhjd->bhij', q, k) * self.scale
        mask_value = -torch.finfo(dots.dtype).max

        if mask is not None:
            mask = F.pad(mask.flatten(1), (1, 0), value = True)
            assert mask.shape[-1] == dots.shape[-1], 'mask has incorrect dimensions'
            mask = mask[:, None, :] * mask[:, :, None]
            dots.masked_fill_(~mask, mask_value)
            del mask

        attn = dots.softmax(dim=-1)

        out = torch.einsum('bhij,bhjd->bhid', attn, v)
        out = rearrange(out, 'b h n d -> b n (h d)')
        out =  self.to_out(out)
        return out

class Transformer(nn.Module):
    def __init__(self, dim, depth, heads, mlp_dim):
        super().__init__()
        self.layers = nn.ModuleList([])
        for _ in range(depth):
            self.layers.append(nn.ModuleList([
                Residual(PreNorm(dim, Attention(dim, heads = heads))),
                Residual(PreNorm(dim, FeedForward(dim, mlp_dim)))
            ]))
    def forward(self, x, mask = None):
        for attn, ff in self.layers:
            x = attn(x, mask = mask)
            x = ff(x)
        return x

import math
def sinusoidal_position_embedding(pos, d):
    position = torch.arange(pos).unsqueeze(1)
    div_term = torch.exp(torch.arange(0, d, 2) * -(math.log(10000.0) / d))
    pe = torch.zeros(pos, d)
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    pe = pe.unsqueeze(0).cuda()
    return pe

class LearnablePositionalEmbedding(nn.Module):
    def __init__(self, num_patches, embed_dim):
        super(LearnablePositionalEmbedding, self).__init__()
        # 定义一个可学习的参数矩阵，形状为 (num_patches, embed_dim)
        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, embed_dim))
    
    def forward(self, x):
        # x: (batch_size, num_patches, embed_dim)
        # 将位置编码添加到输入张量中
        return x + self.pos_embedding

class ViT(nn.Module):
    def __init__(self, *, image_size, patch_size, num_classes, embed_dim, depth, heads, mlp_dim, channels = 3):
        super().__init__()
        assert image_size % patch_size == 0, 'Image dimensions must be divisible by the patch size.'
        num_patches = (image_size // patch_size) ** 2
        patch_dim = channels * patch_size ** 2
        assert num_patches > MIN_NUM_PATCHES, f'your number of patches ({num_patches}) is way too small for attention to be effective (at least 16). Try decreasing your patch size'

        self.patch_size = patch_size

        # self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, embed_dim))
        # self.pos_embedding =  sinusoidal_position_embedding(num_patches + 1, embed_dim)

        self.patch_to_embedding = nn.Linear(patch_dim, embed_dim)

        # 将图像块投影到嵌入空间
        # self.patch_to_embedding = nn.Conv2d(
        #     in_channels=3,  # 假设输入是 RGB 图像
        #     out_channels=embed_dim,
        #     kernel_size=patch_size,
        #     stride=patch_size
        # )
        # 可学习的位置编码
        self.pos_embedding = LearnablePositionalEmbedding(num_patches, embed_dim)


        self.cls_token = nn.Parameter(torch.randn(1, 1, embed_dim))
      

        self.transformer = Transformer(embed_dim, depth, heads, mlp_dim)

        self.to_cls_token = nn.Identity()

        file_name = datetime.now().strftime('%Y%m%d_%H%M%S_ViT.txt')
        with open(file_name, 'a+', encoding='utf-8') as file:
            file.write('image_size = {}\n'.format(image_size))
            file.write('patch_size = {}\n'.format(patch_size))
            file.write('embed_dim = {}\n'.format(embed_dim))
            file.write('depth = {}\n'.format(depth))
            file.write('heads = {}\n'.format(heads))
            file.write('mlp_dim = {}\n'.format(mlp_dim))
            file.close()

    def forward(self, img, mask = None):
        p = self.patch_size
        
        x = rearrange(img, 'b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1 = p, p2 = p)
        # print('vit input', x.shape)
        x = self.patch_to_embedding(x)
        # print('patch_to_embedding', x.shape) # [1, 484, 1024]
        b, n, _ = x.shape
        
        cls_tokens = repeat(self.cls_token, '() n d -> b n d', b = b)
        x = torch.cat((cls_tokens, x), dim=1)
        x += self.pos_embedding.pos_embedding[:, :(n + 1)]
       

        x = self.transformer(x, mask)

        x = self.to_cls_token(x[:,1:,:])
       
        return x

if __name__ =="__main__":

    v = ViT(
        image_size = 1024,
        patch_size = 128,
        num_classes = 1,
        dim = 1024,
        depth = 6,
        heads = 8,
        mlp_dim = 2048,
       
    )
    
    img = torch.randn(1, 3, 1024, 1024)
    mask = torch.ones(1, 8, 8).bool() # optional mask, designating which patch to attend to
    print(v)
    preds = v(img, mask = mask) # (1, 1000)
    print(preds)