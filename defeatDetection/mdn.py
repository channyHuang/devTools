# -*- coding: utf-8 -*-

import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F

# Mixture Density Networks

COEFS = 10
IN_DIM = 1024
OUT_DIM = IN_DIM

# 混合密度网络
class MDN(nn.Module):
    def __init__(self, input_dim=IN_DIM, out_dim=OUT_DIM, layer_size=IN_DIM, coefs=COEFS, test=False, standards=0.5):
        super(MDN, self).__init__()
        self.in_features = input_dim

        self.pi = nn.Linear(layer_size, coefs, bias=False)
        self.mu = nn.Linear(layer_size, out_dim * coefs, bias=False)  # mean
        self.sigma_sq = nn.Linear(layer_size, out_dim * coefs, bias=False)  # isotropic independent variance
        self.out_dim = out_dim
        self.coefs = coefs
        self.test = test
        self.standards = standards

    def forward(self, x):
        ep = np.finfo(float).eps
        x = torch.clamp(x, ep)

        pi = F.softmax(self.pi(x), dim=-1)
        sigma_sq = F.softplus(self.sigma_sq(x)).view(x.size(0),x.size(1),self.in_features, -1)  # logvar
        mu = self.mu(x).view(x.size(0),x.size(1),self.in_features, -1)  # mean
        return pi, mu, sigma_sq


def log_gaussian(x, mean, logvar):
    '''
    Computes the Gaussian log-likelihoods

    Parameters:
        x: [samples,features]  data samples
        mean: [features]  Gaussian mean (in a features-dimensional space)
        logvar: [features]  the logarithm of variances [no linear dependance hypotesis: we assume one variance per dimension]

    Returns:
         [samples]   log-likelihood of each sample
    '''
    x = x.unsqueeze(-1).expand_as(logvar)
    a = (x - mean) ** 2  # works on multiple samples thanks to tensor broadcasting
    log_p = (logvar + a / (torch.exp(logvar))).sum(2)
    log_p = -0.5 * (np.log(2 * np.pi) + log_p)
    
    return log_p 


def log_gmm(x, means, logvars, weights, total=True):
    '''
    Computes the Gaussian Mixture Model log-likelihoods

    Parameters:
        x: [samples,features]  data samples
        means:  [K,features]   means for K Gaussians
        logvars: [K,features]  logarithm of variances for K Gaussians  [no linear dependance hypotesis: we assume one variance per dimension]
        weights: [K]  the weights of each Gaussian
        total:   wether to sum the probabilities of each Gaussian or not (see returning value)

    Returns:
        [samples]  if total=True. Log-likelihood of each sample
        [K,samples] if total=False. Log-likelihood of each sample for each model

    '''
    res = -log_gaussian(x ,means, logvars) # negative of log likelihood
    res = weights * res
    if total:
        return torch.sum(res,2)
    else:
        return res


def mdn_loss_function(x, means, logvars, weights, test=False):
    if test:
        res = log_gmm(x, means, logvars, weights)
    else:
        res = torch.mean(torch.sum(log_gmm(x, means, logvars, weights),1))
    return res

##### Adding Noise ############

def add_noise(latent, noise_type="gaussian", sd=0.2):
    """Here we add noise to the latent features concatenated from the 4 autoencoders.
    Arguements:
    'gaussian' (string): Gaussian-distributed additive noise.
    'speckle' (string) : Multiplicative noise using out = image + n*image, where n is uniform noise with specified mean & variance.
    'sd' (float) : standard deviation used for generating noise

    Input :
        latent : numpy array or cuda tensor.

    Output:
        Array: Noise added input, can be np array or cuda tnesor.
    """
    assert sd >= 0.0
    if noise_type == "gaussian":
        mean = 0.

        n = torch.distributions.Normal(torch.tensor([mean]), torch.tensor([sd]))
        noise = n.sample(latent.size()).squeeze(2).cuda()
        latent = latent + noise
        return latent

    if noise_type == "speckle":
        noise = torch.randn(latent.size()).cuda()
        latent = latent + latent * noise
        return latent
    return latent

if __name__ == "__main__":
    model = MDN()
    model = model.cuda()
    print(model)
