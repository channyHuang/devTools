import os
from pathlib import Path
import random
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms.functional as TF

class ImgDataset(Dataset):
    def __init__(self, img_folder = '../input'):
        self.file_list = []
        file_name_list = os.listdir(img_folder)
        img_ext_list = ['.jpg', '.png', '.bmp']
        for file_name in file_name_list:
            ext = Path(file_name).suffix.lower() 
            for img_ext in img_ext_list:
                if img_ext in ext:
                    self.file_list.append(os.path.join(img_folder, file_name))
                    break

    def __getitem__(self, idx):
        img = Image.open(self.file_list[idx])
        # PNG RGBA 4 channel change to RGB 3 channel
        img = img.convert("RGB")
        return self.transform(img)
    
    def __len__(self):
        return len(self.file_list)
    
    def transform(self, img):
        if random.random() > 0.3:
            angle = random.randint(-60, 60)
            img = TF.rotate(img,angle)
        width, height = img.size
        dw = 32 - (width%32)
        dh = 32 - (height%32)
        img = TF.pad(img,(dw,dh,0,0))
        return TF.to_tensor(img)
    