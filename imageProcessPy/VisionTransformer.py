import torch
import torch.nn as nn
import torch.nn.functional as F

class PatchEmbedding(nn.Module):
    def __init__(self, img_size=1024, patch_size=16, in_channels=3, embed_dim=768):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.n_patches = (img_size // patch_size) ** 2

        self.proj = nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size)

    def forward(self, x):
        x = self.proj(x)  # (B, E, H/P, W/P)
        x = x.flatten(2)  # (B, E, N)
        x = x.transpose(1, 2)  # (B, N, E)
        return x
    
class TransformerEncoder(nn.Module):
    def __init__(self, embed_dim=768, num_heads=12, mlp_ratio=4, dropout=0.1):
        super().__init__()
        self.norm1 = nn.LayerNorm(embed_dim)
        self.attention = nn.MultiheadAttention(embed_dim, num_heads, dropout=dropout)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * mlp_ratio),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(embed_dim * mlp_ratio, embed_dim),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        x = x + self.attention(self.norm1(x), self.norm1(x), self.norm1(x))[0]
        x = x + self.mlp(self.norm2(x))
        return x
    
class VisionTransformer(nn.Module):
    def __init__(self, img_size=1024, patch_size=16, in_channels=3, embed_dim=768, depth=12, num_heads=12, mlp_ratio=4, num_classes = 1000, dropout=0.1):
        super().__init__()
        self.patch_embed = PatchEmbedding(img_size, patch_size, in_channels, embed_dim)
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, self.patch_embed.n_patches + 1, embed_dim))
        self.dropout = nn.Dropout(dropout)
        self.encoder = nn.ModuleList([
            TransformerEncoder(embed_dim, num_heads, mlp_ratio, dropout)
            for _ in range(depth)
        ])
        self.norm = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, num_classes)

    def forward(self, x):
        B = x.shape[0]
        x = self.patch_embed(x)  # (B, N, E)
        cls_token = self.cls_token.expand(B, -1, -1)  # (B, 1, E)
        x = torch.cat((cls_token, x), dim=1)  # (B, N+1, E)
        x = x + self.pos_embed
        x = self.dropout(x)

        for layer in self.encoder:
            x = layer(x)

        x = self.norm(x)
        cls_token_final = x[:, 0]  # (B, E)
        out = self.head(cls_token_final)  # (B, num_classes)
        return out
    
if __name__ =="__main__":
    model = VisionTransformer(img_size=1024, patch_size=16, in_channels=3, embed_dim=768, depth=12, num_heads=12, mlp_ratio=4, num_classes=1000)

    img = torch.randn(1, 3, 1024, 1024)
    print('input shape', img.shape)
    output = model(img)
    print('output shape', output.shape)
