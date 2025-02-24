# -*- coding: utf-8 -*-

import torch
import torch.nn as nn

# 图像解码
class Decoder(nn.Module):
    def __init__(self, in_channels):
        super(Decoder, self).__init__()

        self.decoder1280 = nn.Sequential(
            nn.ConvTranspose2d(in_channels= in_channels, out_channels=16, kernel_size= 2, stride=2,padding=1),  # In b, 8, 8, 8 >> out b, 16, 15, 15
            nn.BatchNorm2d(16, affine = True),
            nn.LeakyReLU(True),    

            nn.ConvTranspose2d(16, 32, 3, stride=4, padding = 1),  #out> b,32, 49, 49
            nn.BatchNorm2d(32, affine = True),
            nn.LeakyReLU(True),             
            nn.ConvTranspose2d(32, 32, 3, stride=2, padding=1),  #out> b, 32, 245, 245
            nn.BatchNorm2d(32, affine = True),
            nn.LeakyReLU(True), 
            nn.ConvTranspose2d(32, 16, 3, stride=2),  #out> b, 16, 497, 497
            nn.BatchNorm2d(16, affine = True),
            nn.LeakyReLU(True), 
            nn.ConvTranspose2d(16, 8, 2, stride=1),  #out> b, 8, 502, 502
            nn.BatchNorm2d(8, affine = True),
            nn.LeakyReLU(True),
            nn.ConvTranspose2d(8, 3, 5, stride=2),  #out> b, 3, 512, 512
            nn.BatchNorm2d(3, affine = True),
            nn.LeakyReLU(True),
            nn.ConvTranspose2d(3, 3, 2, stride=3),  #out> b, 3, 1280, 1280
            nn.Tanh()
            )
        
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(in_channels= in_channels, out_channels=16, kernel_size= 3, stride=2,padding=1),  # In b, 8, 8, 8 >> out b, 16, 15, 15
            nn.BatchNorm2d(16, affine = True),
            nn.LeakyReLU(True),    

            nn.ConvTranspose2d(16, 32, 4, stride=2, padding = 1),  #out> b,32, 49, 49
            nn.BatchNorm2d(32, affine = True),
            nn.LeakyReLU(True),             
            nn.ConvTranspose2d(32, 32, 2, stride=2, padding=1),  #out> b, 32, 245, 245
            nn.BatchNorm2d(32, affine = True),
            nn.LeakyReLU(True), 
            nn.ConvTranspose2d(32, 16, 3, stride=2),  #out> b, 16, 497, 497
            nn.BatchNorm2d(16, affine = True),
            nn.LeakyReLU(True), 
            nn.ConvTranspose2d(16, 8, 2, stride=2),  #out> b, 8, 502, 502
            nn.BatchNorm2d(8, affine = True),
            nn.LeakyReLU(True),
            nn.ConvTranspose2d(8, 3, 4, stride=3),  #out> b, 3, 512, 512
            nn.BatchNorm2d(3, affine = True),
            nn.LeakyReLU(True),
            nn.ConvTranspose2d(3, 3, 4, stride=2),  #out> b, 3, 1280, 1280
            nn.Tanh()
            )
        
    def forward(self, x): 
        # [4, 16, 8, 8] -> [4, 3, 1024, 1024]
        recon = self.decoder(x)
        return recon
    
if __name__=="__main__":
    decoder = Decoder(16)
    input = torch.randn(4, 16, 8, 8)
    output = decoder(input)
    print('output shape', output.shape)