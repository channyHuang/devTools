import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 加载数据集
dataset = datasets(root='./../dataset_train/class3_4_val/train/good', train=True, download=False, transform=transforms.ToTensor())

# 计算均值和标准差
def compute_mean_std(dataset):
    loader = DataLoader(dataset, batch_size=len(dataset), shuffle=False)
    data = next(iter(loader))[0]  # 获取所有数据
    mean = torch.mean(data, dim=(0, 2, 3))  # 计算每个通道的均值
    std = torch.std(data, dim=(0, 2, 3))    # 计算每个通道的标准差
    return mean, std

mean, std = compute_mean_std(dataset)
print(f"Mean: {mean}, Std: {std}")