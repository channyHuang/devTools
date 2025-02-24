from datetime import datetime
import os
import torch
import torch.nn.functional as F
from torch.optim import Adam

from encode_decode import EncodeDecode
from config import config
import mvtech
from ssim import SSIM
import mdn

ssim_loss = SSIM()

#Dataset
data = mvtech.Mvtec(config.batch_size, product = config.product)

def trainEncodeDecode():
    model = EncodeDecode(patch_size = config.patch_size, train = True).cuda()
    model.train()

    #Optimiser Declaration
    Optimiser = Adam(list(model.parameters()), lr = config.learning_rate, weight_decay=0.0001)

    minloss = 1e10

    print('\nNetwork training started.....')
    for epoch in range(config.epochs):
        print('epoch {}/{}, pre epoches min loss {}'.format(epoch, config.epochs, minloss), end='\r')

        for image, mask in data.train_loader:
            if image.size(1)==1:
                image = torch.stack([image, image, image]).squeeze(2).permute(1,0,2,3)
            model.zero_grad()
            
            vector, reconstructions = model(image.cuda())
            
            loss1 = F.mse_loss(reconstructions, image.cuda(), reduction='mean') #Rec Loss
            loss2 = -ssim_loss(image.cuda(), reconstructions) #1 - [-1,1]
            alpha = 0.5
            loss = alpha * loss1 + (1 - alpha) * loss2
            
            #Optimiser step
            loss.backward()
            Optimiser.step()

        for image, mask in data.test_anom_loader:
            if image.size(1)==1:
                image = torch.stack([image, image, image]).squeeze(2).permute(1,0,2,3)
            model.zero_grad()
            
            vector, reconstructions = model(image.cuda())
            
            loss1 = F.mse_loss(reconstructions, image.cuda(), reduction='mean') #Rec Loss
            loss2 = -ssim_loss(image.cuda(), reconstructions) #1 - [-1,1]
            alpha = 0.5
            loss = alpha * loss1 + (1 - alpha) * loss2
            
            #Optimiser step
            loss.backward()
            Optimiser.step()

        for image, mask in data.test_norm_loader:
            if image.size(1)==1:
                image = torch.stack([image, image, image]).squeeze(2).permute(1,0,2,3)
            model.zero_grad()
            
            vector, reconstructions = model(image.cuda())
            
            loss1 = F.mse_loss(reconstructions, image.cuda(), reduction='mean') #Rec Loss
            loss2 = -ssim_loss(image.cuda(), reconstructions) #1 - [-1,1]
            alpha = 0.5
            loss = alpha * loss1 + (1 - alpha) * loss2
            
            #Optimiser step
            loss.backward()
            Optimiser.step()

        if loss <= minloss:
            minloss = loss
            os.makedirs('./saved_model', exist_ok=True)
            torch.save(model.state_dict(), f'./saved_model/EncodeDecode_{config.product}'+'.pt')

            # with open('minloss.txt', 'a+', encoding='utf-8') as file:
            #     file.write(datetime.now().strftime('%Y%m%d_%H%M%S'))
            #     file.write('\n')
            #     file.write('minloss = {}'.format(minloss))
            #     file.write('\n')
            #     file.close()

def trainMDN():
    G_estimate = mdn.MDN().cuda()
    G_estimate.train()

    minloss = 1e10

    model = EncodeDecode(patch_size = config.patch_size, train = True).cuda()
    model.load_state_dict(torch.load(f'./saved_model/EncodeDecode_{config.product}'+'.pt'))

    Optimiser = Adam(list(G_estimate.parameters()), lr = config.learning_rate, weight_decay=0.0001)

    print('\nNetwork training started.....')
    for epoch in range(config.epochs):
        print('epoch {}/{}, pre epoches min loss {}'.format(epoch, config.epochs, minloss), end='\r')

        for image, mask in data.train_loader:
            if image.size(1)==1:
                image = torch.stack([image, image, image]).squeeze(2).permute(1,0,2,3)
            G_estimate.zero_grad()

            vector, reconstructions = model(image.cuda())
            pi, mu, sigma = G_estimate(vector)

            loss = mdn.mdn_loss_function(vector, mu, sigma, pi)
            loss.backward()

            Optimiser.step()

        if loss <= minloss:
            minloss = loss
            os.makedirs('./saved_model', exist_ok=True)
            torch.save(G_estimate.state_dict(), f'./saved_model/G_estimate_{config.product}'+'.pt')

            # with open('minloss_G.txt', 'a+', encoding='utf-8') as file:
            #     file.write(datetime.now().strftime('%Y%m%d_%H%M%S'))
            #     file.write('   minloss = {}\n'.format(minloss))
            #     file.close()

def train():
    trainEncodeDecode()
    trainMDN()

if __name__ == "__main__":
    train()
