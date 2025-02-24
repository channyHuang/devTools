# -*- coding: utf-8 -*-

import torch
import torch.nn as nn

from vit import ViT
from decoder import Decoder
from digitcaps import DigitCaps
from VisionTransformer_own import VisionTransformer

# 图像编解码
class EncodeDecode(nn.Module):
    def __init__(self, image_size = 1408,
                    patch_size = 64,
                    num_classes = 1,
                    embed_dim = 1024,
                    depth = 6,
                    heads = 8,
                    mlp_dim = 2048,
                    train= True):

        super(EncodeDecode, self).__init__()

        self.vt = ViT(
            image_size = image_size,
            patch_size = patch_size,
            num_classes = num_classes,
            embed_dim = embed_dim,
            depth = depth,
            heads = heads,
            mlp_dim = mlp_dim )
        
        # self.vt = VisionTransformer(
        #     img_size= image_size, 
        #     patch_size= patch_size, 
        #     in_channels=3, 
        #     embed_dim=embed_dim, 
        #     depth= depth, 
        #     num_heads= heads, 
        #     mlp_ratio= 4, 
        #     num_classes = 1, 
        #     dropout=0.1)
     
        self.decoder = Decoder(16)
        # self.decoder = model_ShuffleNetV2.ShuffleNetV2()
        # self.G_estimate= mdn1.MDN() # Trained in modular fashion
        self.Digcap = DigitCaps(in_num_caps=((image_size//patch_size)**2)*8*8, in_dim_caps=16)
        self.mask = torch.ones(1, image_size//patch_size, image_size//patch_size).bool().cuda()
        self.Train = train
        
        if self.Train:
            print("\nInitializing network weights.........")
            self.initialize_weights(self.vt, self.decoder)

    def forward(self,x):
        b = x.size(0)
        encoded = self.vt(x, self.mask)
        # encoded = self.vt(x)
        if self.Train:
            encoded = add_noise(encoded)
        # print('vit encode', encoded.shape, encoded.view(b,encoded.size(1)*8*8,-1).shape) # [1, 484, embed_dim]
        encoded1, vectors = self.Digcap(encoded.view(b,encoded.size(1)*8*8,-1))
        # print('encode ', encoded1.view(b,-1,8,8).shape) # [1, 16, 8, 8]
        recons = self.decoder(encoded1.view(b,-1,8,8))
        # print('recons', recons.shape) # [batch_size, 3, 1408, 1408]
        # pi, mu, sigma = self.G_estimate(encoded)       
        # return encoded, pi, sigma, mu, recons
            
        return encoded, recons
    
    # Initialize weight function
    def initialize_weights(*models):
        for model in models:
            for module in model.modules():
                if isinstance(module, nn.Conv2d) or isinstance(module, nn.Linear):
                    nn.init.kaiming_normal_(module.weight)
                    if module.bias is not None:
                        module.bias.data.zero_()
                elif isinstance(module, nn.BatchNorm2d):
                    module.weight.data.fill_(1)
                    module.bias.data.zero_()

def add_noise(latent, noise_type="gaussian", sd=0.2):
    """Here we add noise to the latent features concatenated from the 4 autoencoders.
    Arguements:
    'gaussian' (string): Gaussian-distributed additive noise.
    'speckle' (string) : Multiplicative noise using out = image + n*image, where n is uniform noise with specified mean & variance.
    'sd' (integer) : standard deviation used for geenrating noise

    Input :
        latent : numpy array or cuda tensor.

    Output:
        Array: Noise added input, can be np array or cuda tnesor.
    """
    assert sd >= 0.0
    if noise_type == "gaussian":
        mean = 0.

        n = torch.distributions.Normal(torch.tensor([mean]), torch.tensor([sd]))
        noise = n.sample(latent.size()).squeeze(-1).cuda()
        latent = latent + noise
        return latent

    if noise_type == "speckle":
        noise = torch.randn(latent.size()).cuda()
        latent = latent + latent * noise
        return latent

if __name__ == "__main__":
    from torchsummary import summary
    mod = EncodeDecode(image_size = 1408,
                    patch_size = 128,
                    num_classes = 1,
                    dim = 1024,
                    depth = 6,
                    heads = 8,
                    mlp_dim = 2048,
                    train= True).cuda()
    summary(mod, (3, 1408, 1408))