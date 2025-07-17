import argparse
import os
import time
import warnings

from model.Encoder import *
from model.Decoder import *

warnings.filterwarnings('ignore')

# 压缩编码或解压解码图像集

def parseParam():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', nargs='?', default='./out/train_state_new0.91455.tar', help='Path for model checkpoint file [default: ./out/main.tar]')
    parser.add_argument('--encode', nargs='?', default=True, help='encode or decode: True or False')
    parser.add_argument('--image_folder', nargs='?', default='./dataset/', help='Directory which holds the images to be compressed [default: ./dataset/]')
    parser.add_argument('--compress_folder', nargs='?', default='./out/compressed', help='Directory which holds the compressed files')
    parser.add_argument('--decompress_folder', nargs='?', default='./out/decompressed/', help='Directory which will hold the decompressed images')
    args = parser.parse_args()
    return args

def encode_folder(args):
    encoder = Encoder(args.model)

    file_list = os.listdir(args.image_folder)
    begin_time = time.time()
    for file_name in file_list:
        file_path = os.path.join(args.image_folder, file_name)
        out_file_name = os.path.join(args.compress_folder, '%s.xfr'%file_name[:-4])
        start_time = time.time()
        encoder.encode_and_save(file_path, out_file_name)
        print('%s file encode cost %.2f seconds'%(file_name, time.time() - start_time))
    print('average cost %.2f seconds'%((time.time() - begin_time) / len(file_list)))

def decode_folder(args):
    decoder = Decoder(args.model)
    file_list = os.listdir(args.compress_folder)
    begin_time = time.time()
    for file_name in file_list:
        file_path = os.path.join(args.compress_folder, file_name)
        out_file_name = os.path.join(args.decompress_folder, '%s.png'%file_name[:-4])

        start_time = time.time()
        decoder.decompress(file_path, out_file_name)
        print('%s file decode cost %.2f seconds'%(file_name, time.time() - start_time))
    print('average cost %.2f seconds'%((time.time() - begin_time) / len(file_list)))

if __name__ == '__main__':
    args = parseParam()
    if args.encode == True:
        encode_folder(args)
    else:
        decode_folder(args)
    