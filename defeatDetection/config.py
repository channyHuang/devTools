# -*- coding: utf-8 -*-

import torch

class Config():
    def __init__(self):
        self.USE_CUDA = True and torch.cuda.is_available()

        self.product = 'class2_9'
        self.epochs = 50
        self.learning_rate = 0.0001
        self.patch_size = 64
        self.batch_size = 1

        self.min_loss = 1e10

config = Config()