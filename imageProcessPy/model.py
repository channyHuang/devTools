import torch
import torch.nn as nn
import torch.nn.functional as F

class Unity(nn.Module):
    def __init__(self, nInChannel = 16, nOutChannel = 32, nKernelSize = 3, nStride = 2, nPadding = 1):
        super(Unity, self).__init__()

        self.conv = nn.Conv2d(in_channels=nInChannel, out_channels = nOutChannel, kernel_size = nKernelSize, stride = nStride, padding=nPadding)
        self.bn = nn.BatchNorm2d(nOutChannel, affine=True)
        self.relu = F.relu()

    def forward(self, x):
        slope = 0.2
        return self.relu(self.bn(self.conv(x)), slope)

class UnityTranspose(nn.Module):
    def __init__(self, nInChannel = 16, nOutChannel = 32, nKernelSize = 3, nStride = 2, nPadding = 1):
        super(Unity, self).__init__()

        self.conv = nn.ConvTranspose2d(in_channels=nInChannel, out_channels = nOutChannel, kernel_size = nKernelSize, stride = nStride, padding=nPadding)
        self.bn = nn.BatchNorm2d(nOutChannel, affine=True)
        self.relu = F.leaky_relu()

    def forward(self, x):
        slope = 0.2
        return self.relu(self.bn(self.conv(x)), slope)

class SeqModel(nn.Module):
    def __init__(self):
        super().__init__()
        slope = 0.2
        self.model = nn.Sequential(
            nn.ConvTranspose2d(in_channels=1, out_channels=48, kernel_size=(11, 11), stride=(1, 1), padding=5),
            nn.BatchNorm2d(48),
            nn.LeakyReLU(negative_slope=slope),
            nn.Conv2d(in_channels=48, out_channels=48, kernel_size=(9, 9), stride=(2, 2), padding=4),
            nn.BatchNorm2d(48),
            nn.LeakyReLU(negative_slope=slope),
            nn.Conv2d(in_channels=48, out_channels=48, kernel_size=(7, 7), stride=(2, 2), padding=3),
            nn.BatchNorm2d(48),
            nn.LeakyReLU(negative_slope=slope),
            nn.Conv2d(in_channels=48, out_channels=48, kernel_size=(5, 5), stride=(2, 2), padding=2),
            nn.BatchNorm2d(48),
            nn.LeakyReLU(negative_slope=slope),
            nn.Conv2d(in_channels=48, out_channels=48, kernel_size=(3, 3), stride=(2, 2), padding=1),
            nn.BatchNorm2d(48),
            nn.LeakyReLU(negative_slope=slope),

            nn.ConvTranspose2d(in_channels=48, out_channels=48, kernel_size=(5, 5), stride=(2, 2), padding=2, output_padding=1),
            nn.BatchNorm2d(48),
            nn.ReLU(),
            nn.ConvTranspose2d(in_channels=96, out_channels=48, kernel_size=(7, 7), stride=(2, 2), padding=3, output_padding=1),
            nn.BatchNorm2d(48),
            nn.ReLU(),
            nn.ConvTranspose2d(in_channels=96, out_channels=48, kernel_size=(9, 9), stride=(2, 2), padding=4, output_padding=1),
            nn.BatchNorm2d(48),
            nn.ReLU(),
            nn.ConvTranspose2d(in_channels=96, out_channels=48, kernel_size=(11, 11), stride=(2, 2), padding=5, output_padding=1),
            nn.BatchNorm2d(48),
            nn.ReLU(),

            nn.Conv2d(in_channels=96, out_channels=1, kernel_size=(1, 1), stride=(1, 1)),
            nn.BatchNorm2d(),
            nn.Tanh()
        )

class MyModel1280(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.ConvTranspose2d(in_channels=16, out_channels=16, kernel_size=2, stride=2, padding=1)
        self.bn1 = nn.BatchNorm2d(16, affine=True)
        # self.relu1 = nn.ReLU(True)

        self.conv2 = nn.ConvTranspose2d(16, 32, 3, stride=4, padding=1)
        self.bn2 = nn.BatchNorm2d(32, affine=True)

        self.conv3 = nn.ConvTranspose2d(32, 32, 3, stride=2, padding=1)
        self.bn3 = nn.BatchNorm2d(32, affine=True)

        self.conv4 = nn.ConvTranspose2d(32, 16, 3, stride=2)
        self.bn4 = nn.BatchNorm2d(16, affine=True)

        self.conv5 = nn.ConvTranspose2d(16, 8, 2, stride=1)
        self.bn5 = nn.BatchNorm2d(8, affine=True)

        self.conv6 = nn.ConvTranspose2d(8, 3, 5, stride=2)
        self.bn6 = nn.BatchNorm2d(3, affine=True)

        self.last_conv = nn.ConvTranspose2d(3, 3, 2, stride=3)
        self.last_bn = nn.Tanh()

    def forward(self, x):
        slope = 0.2
        print('in x', x.shape) # [4, 16, 8, 8]
        x = F.leaky_relu(self.bn1(self.conv1(x)), slope)
        print('in 2 x ', x.shape) # [4, 16, 15, 15]
        x = F.leaky_relu(self.bn2(self.conv2(x)), slope)
        print('in 3 x ', x.shape) # [4, 32, 49, 49]
        x = F.leaky_relu(self.bn3(self.conv3(x)), slope)
        print('in 4 x ', x.shape) #(4, 32, 245, 245)
        x = F.leaky_relu(self.bn4(self.conv4(x)), slope)
        print('in 5 x ', x.shape) # [4, 16, 497, 497]
        x = F.leaky_relu(self.bn5(self.conv5(x)), slope)
        print('in 6 x ', x.shape) # [4, 8, 1001, 1001]
        x = F.leaky_relu(self.bn6(self.conv6(x)), slope)
        print('after conv6', x.shape)
        x = F.leaky_relu(self.last_bn(self.last_conv(x)), slope)
        print('out ', x.shape) # [4, 3, 1024, 1024]
        return x
    
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.ConvTranspose2d(in_channels=16, out_channels=16, kernel_size=3, stride=2, padding=1)
        self.bn1 = nn.BatchNorm2d(16, affine=True)
        # self.relu1 = nn.ReLU(True)

        self.conv2 = nn.ConvTranspose2d(16, 32, 4, stride=2, padding=1)
        self.bn2 = nn.BatchNorm2d(32, affine=True)

        self.conv3 = nn.ConvTranspose2d(32, 32, 2, stride=2, padding=1)
        self.bn3 = nn.BatchNorm2d(32, affine=True)

        self.conv4 = nn.ConvTranspose2d(32, 16, 3, stride=2)
        self.bn4 = nn.BatchNorm2d(16, affine=True)

        self.conv5 = nn.ConvTranspose2d(16, 8, 2, stride=2)
        self.bn5 = nn.BatchNorm2d(8, affine=True)

        self.conv6 = nn.ConvTranspose2d(8, 3, 4, stride=3)
        self.bn6 = nn.BatchNorm2d(3, affine=True)

        self.last_conv = nn.ConvTranspose2d(3, 3, 4, stride=2)
        self.last_bn = nn.Tanh()

    def forward(self, x):
        slope = 0.2
        print('in x', x.shape) # [4, 16, 8, 8]
        x = F.leaky_relu(self.bn1(self.conv1(x)), slope)
        print('in 2 x ', x.shape) # [4, 16, 15, 15]
        x = F.leaky_relu(self.bn2(self.conv2(x)), slope)
        print('in 3 x ', x.shape) # [4, 32, 49, 49]
        x = F.leaky_relu(self.bn3(self.conv3(x)), slope)
        print('in 4 x ', x.shape) #(4, 32, 245, 245)
        x = F.leaky_relu(self.bn4(self.conv4(x)), slope)
        print('in 5 x ', x.shape) # [4, 16, 497, 497]
        x = F.leaky_relu(self.bn5(self.conv5(x)), slope)
        print('in 6 x ', x.shape) # [4, 8, 1001, 1001]
        x = F.leaky_relu(self.bn6(self.conv6(x)), slope)
        print('after conv6', x.shape)
        x = F.leaky_relu(self.last_bn(self.last_conv(x)), slope)
        print('out ', x.shape) # [4, 3, 1024, 1024]
        return x

class ShuffleModel(nn.Module):
    def __init__(self):
        super().__init__()
        inp = 16
        mid = 32
        out = 16

        self.conv1 = nn.ConvTranspose2d(in_channels=inp, out_channels=mid, kernel_size=3, stride=2, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(mid, affine=True)
        # self.relu1 = nn.ReLU(True)

        self.conv2 = nn.ConvTranspose2d(mid, mid, 2, stride=2, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(mid, affine=True)

        self.conv3 = nn.ConvTranspose2d(mid, out, 3, stride=2, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out, affine=True)

        # inp = 48
        # mid_channels = 24
        # ksize = 3
        # stride = 1
        # pad = 0
        # outputs = 48
        # branch_main = [
        #     # pw
        #     nn.ConvTranspose2d(inp, mid_channels, 3, 1, 0, bias=False),
        #     nn.BatchNorm2d(mid_channels, affine=True),
        #     nn.LeakyReLU(inplace=True),
        #     # dw
        #     nn.ConvTranspose2d(mid_channels, mid_channels, ksize, stride, pad, groups=mid_channels, bias=False),
        #     nn.BatchNorm2d(mid_channels, affine=True),
        #     nn.LeakyReLU(inplace = True),
        #     # pw-linear
        #     nn.ConvTranspose2d(mid_channels, outputs, 3, 1, 0, bias=False),
        #     nn.BatchNorm2d(outputs, affine=True),
        #     nn.LeakyReLU(inplace=True),
        # ]
        # self.branch_main = nn.Sequential(*branch_main)

    def forward(self, x):
        # self.branch_main(x)
        # return x
        # slope = 0.2
        print('in x', x.shape) # [4, 16, 8, 8]
        x = F.leaky_relu(self.bn1(self.conv1(x)))
        print('in 2 x ', x.shape) # [4, 16, 15, 15]
        x = F.leaky_relu(self.bn2(self.conv2(x)))
        print('in 3 x ', x.shape) # [4, 32, 49, 49]
        x = F.leaky_relu(self.bn3(self.conv3(x)))
        print('out ', x.shape) # [4, 3, 1024, 1024]
        return x

if __name__ == '__main__':
    x = torch.rand([4, 16, 8, 8])
    # x = torch.rand([4, 24, 21, 21])
    # model = ShuffleModel()
    model = MyModel()
    y = model(x)
    print('y ', y.shape)