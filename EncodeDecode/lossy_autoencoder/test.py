import argparse
import math
import numpy as np
import os
from PIL import Image

# 计算平均压缩比

def psnr(img1, img2):
    mse = np.mean( (img1 - img2) ** 2 )
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

def parseParam():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-folder', nargs='?', default='./dataset', help='Root directory of Images')
    parser.add_argument('--compress_folder', nargs='?', default='./out/compressed', help='Directory which holds the compressed files')
    parser.add_argument('--decompress_folder', nargs='?', default='./out/decompressed/', help='Directory which will hold the decompressed images')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parseParam()

    file_list = os.listdir(args.dataset_folder)
    tot_pix = 0
    s = 0
    for file_name in file_list:
        origin_path = os.path.join(args.dataset_folder, file_name)
        compress_path = os.path.join(args.compress_folder, file_name)
        decompress_path = os.path.join(args.decompress_folder, file_name)
        
        psnr_val = psnr(np.asarray(Image.open(origin_path)), np.asarray(Image.open(decompress_path)))
        
        img = Image.open(origin_path)
        width, height = img.size
        pixels = width * height
        tot_pix = tot_pix + pixels
        s += psnr_val
        print(' PSNR value is %s'%psnr_val)

    avg = s/len(file_list)
    print('Average PSNR ratio is: %s'%avg)
    orig_size = sum(os.path.getsize(os.path.join(args.dataset_folder, f)) for f in os.listdir('dataset')) 
    comp_size = sum(os.path.getsize(os.path.join(args.compress_folder, f)) for f in os.listdir(args.compress_folder) if '.xfr' in f)
    comp_ratio = orig_size/comp_size

    print(orig_size)
    print(comp_ratio)

    print('Compression ratio is %s'%comp_ratio)
    print('Original data rate is %s'%(orig_size/tot_pix))
    print('compressed data rate is %s'%(comp_size/tot_pix))
