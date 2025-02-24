from encode_decode import EncodeDecode
import numpy as np

import torch
import torch.nn.functional as F

from config import config
import mvtech
from ssim import SSIM
import mdn
from utils import *

ssim_loss = SSIM()

def testEncodeDecode():
    minloss = 0
    model = EncodeDecode(patch_size = config.patch_size, train = True).cuda()
    model.load_state_dict(torch.load(f'./saved_model/EncodeDecode_{config.product}'+'.pt'))

    #Dataset
    data = mvtech.Mvtec(1, product = config.product)

    model.eval()

    for c, (image, mask) in enumerate(data.test_anom_loader):
        vector, reconstructions = model(image.cuda())

        loss1 = F.mse_loss(reconstructions, image.cuda(), reduction='mean') #Rec Loss
        loss2 = -ssim_loss(image.cuda(), reconstructions) #1 - [-1,1]
        print('loss = ', loss1, loss2)
        res = reconstructions.squeeze(0).permute(1, 2, 0).cpu().detach().numpy()
        print(res.shape)
        plot(image, res)

def testMDN():
    G_estimate = mdn.MDN().cuda()
    G_estimate.load_state_dict(torch.load(f'./saved_model/G_estimate_{config.product}'+'.pt'))

    minloss = 1e10

    model = EncodeDecode(patch_size = config.patch_size, train = True).cuda()
    model.load_state_dict(torch.load(f'./saved_model/EncodeDecode_{config.product}'+'.pt'))

    G_estimate.eval()
    model.eval()

    data = mvtech.Mvtec(1, product = config.product)

    for c, (image, mask) in enumerate(data.test_anom_loader):
        vector, reconstructions = model(image.cuda())
        
        pi, mu, sigma = G_estimate(vector)

        loss = mdn.mdn_loss_function(vector, mu, sigma, pi, test=True)
        
        m = torch.nn.UpsamplingBilinear2d((1408, 1408))
        norm_loss_t = loss.detach().cpu().numpy()
        norm_score = norm_loss_t.reshape(-1,1, 1408//config.patch_size, 1408//config.patch_size)

        score_map = m(torch.tensor(norm_score))
        score_map = Filter(score_map , type =0) 
        plot(image, score_map[0][0])

def test():
    # testEncodeDecode()
    testMDN()

if __name__ == "__main__":
    test()