import argparse
import numpy as np
import time
import torch
import torch.nn as nn
from torch.utils.data.sampler import SubsetRandomSampler
import warnings

from model.ImgDataset import ImgDataset
from model.Autoencoder import Autoencoder
from model.ModelManager import *
from utils.evaluation import *

warnings.filterwarnings('ignore')

def train(train_params,epoch,model=None,optimizer=None,criterion=None,history=None,train_loader=None,validation_loader=None):
  while epoch<=train_params['stop_epoch']:
    total_loss = 0
    total_accuracy = 0
    model.train()
    train_params['exp_lr_scheduler'].step()
    print('Epoch: {}\tLR: {:.5f}'.format(epoch,train_params['exp_lr_scheduler'].get_lr()[0]))
    for batch_idx, data in enumerate(train_loader):
      target = data
      if torch.cuda.is_available():
        data = data.cuda()
        target = target.cuda()
      # forward
      output = model(data)
      # backward + optimize
      loss = criterion(output, target)
      optimizer.zero_grad()
      loss.backward()
      optimizer.step()
      # print statistics
      total_loss+=loss.item()
      # print('Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.5f}'.format(epoch, (batch_idx + 1) * len(data), len(train_params['train_indices']),100*(batch_idx + 1)* len(data) / len(train_params['train_indices']), loss))
    print('Train Loss:\t%.6f'%(total_loss*train_params['batch_size']/len(train_params['train_indices'])))
    vloss, vaccuracy = validate(model,criterion,validation_loader)
    print('Validation Loss:\t%.6f'%(vloss*train_params['batch_size']/len(train_params['val_indices'])))
    history['train_losses'].append((total_loss*train_params['batch_size'])/len(train_params['train_indices']))
    history['val_losses'].append((vloss*train_params['batch_size'])/len(train_params['val_indices']))
    history['epoch_data'].append(epoch)
#     visualize()
    epoch=1+epoch

batch_size = 1
# 验证数据集比例
validation_split = 0.1
random_seed= 42
START_EPOCH = 1
shuffle_dataset = True
history = {
    'train_losses':[],
    'val_losses' :[],
    'epoch_data' : []
}

def parseParams():
    parser = argparse.ArgumentParser()

    # parser.add_argument('--dataset-path', nargs='?', default='/home/channy/Documents/datasets/0821_dataset/train/images', help='Root directory of Images')
    parser.add_argument('--dataset-path', nargs='?', default='./dataset', help='Root directory of Images')
    parser.add_argument('--checkpoint-path', nargs='?', default='out/main.tar', help='Use to resume training from last checkpoint')
    parser.add_argument('--stop-at',nargs='?',default=90,help='Epoch after you want to end training',type=int)
    parser.add_argument('--save-at', nargs='?', default='out/', help='Directory where training state will be saved')
    args = parser.parse_args()

    return args

args = parseParams()

model = Autoencoder().float()
criterion = nn.SmoothL1Loss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
exp_lr_scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[100,150,180], gamma=0.1)
if torch.cuda.is_available():
    model = model.cuda()

# 加载历史训练结果
if(args.checkpoint_path):
    checkpoint = load_checkpoint(args.checkpoint_path)
    model.load_state_dict(checkpoint['model_state'])
    optimizer.load_state_dict(checkpoint['optimizer_state'])
    history = checkpoint['history']
    START_EPOCH = history['epoch_data'][-1]+1
    
ds = ImgDataset(img_folder=args.dataset_path)

# 创建训练和验证数据集
dataset_size = len(ds)
indices = list(range(dataset_size))
split = int(np.floor(validation_split * dataset_size))
if shuffle_dataset :
    np.random.seed(random_seed)
    np.random.shuffle(indices)
train_indices, val_indices = indices[split:], indices[:split]


# 创建数据加载器
train_sampler = SubsetRandomSampler(train_indices)
validation_sampler = SubsetRandomSampler(val_indices)
train_loader = torch.utils.data.DataLoader(ds,batch_size=batch_size,sampler=train_sampler)
validation_loader = torch.utils.data.DataLoader(ds, batch_size=batch_size,sampler=validation_sampler)

parameters = {
    'stop_epoch': args.stop_at,
    'exp_lr_scheduler' : exp_lr_scheduler,
    'train_indices' : train_indices,
    'val_indices' : val_indices,
    'batch_size' : batch_size
}

print('GPU Support Found: %s'%torch.cuda.is_available())

start = time.time()
print('Begining training...')

train(parameters,START_EPOCH,model=model,optimizer=optimizer,criterion=criterion,history=history,train_loader=train_loader,validation_loader=validation_loader)
end = time.time()
print('Finished training in %s seconds'%(end-start))

vds = ImgDataset(img_folder=args.dataset_path)
total_score=0
for i in range(0,len(vds)):
    total_score += evaluate(model,vds,i)
avg_score = '%.5f'%(total_score/len(vds))
print('Average MSSSIM on validation is %s'%avg_score)

save_checkpoint({
    'history' : history,
    'model_state' :model.state_dict(),
    'optimizer_state' : optimizer.state_dict(),
},args.save_at+'train_state_new%s.tar'%avg_score)

torch.save(model, 'LossyImageCompression.pth')

visualize(history)