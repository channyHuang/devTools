import os
import cv2
import numpy as np

def align(x, a):
    return (x + a - 1) & ~(a - 1)

def resizeImage(image_path = '/home/channy/Downloads/defect_origin/9_27.jpg'):
    dst_path = '/home/channy/Downloads/defect_test/9_27.jpg'

    origin_image = cv2.imread(image_path)
    nAddWidth = align(origin_image.shape[1], 16)
    nAddHeight = align(origin_image.shape[0], 16)
    new_image = cv2.copyMakeBorder(origin_image, 0, nAddHeight - origin_image.shape[0], 0, nAddWidth - origin_image.shape[1], cv2.BORDER_CONSTANT, (0, 0, 0))
    cv2.imwrite(dst_path, new_image)

def resizeFolder(image_folder = './ownDataset/traindir/train', dst_folder = './traindir/train'):
    image_list = os.listdir(image_folder)
    for i, image_name in enumerate(image_list):
        print('infer {} / {}'.format(i+1, len(image_list)), end='\r')
        image_path = os.path.join(image_folder, image_name)
        origin_image = cv2.imread(image_path)
        nAddWidth = align(origin_image.shape[1], 16)
        nAddHeight = align(origin_image.shape[0], 16)
        # print(nAddWidth, nAddHeight)
        new_image = cv2.copyMakeBorder(origin_image, 0, nAddHeight - origin_image.shape[0], 0, nAddWidth - origin_image.shape[1], cv2.BORDER_CONSTANT, (0, 0, 0))
        # print(new_image.shape)
        cv2.imwrite(os.path.join(dst_folder, image_name), new_image)

    print('end')

# class 1
def copyFolder():
    image_folder = '/home/channy/Downloads/dataset_defect/5/10'
    dst_folder = '/home/channy/Downloads/traindir/train'
    lastIdx = [1, 4, 7, 10]
    for i in range(1, 53):
        for j in range(1, 2):
            for k in lastIdx:
                name = "{}_{}_{}.jpg".format(i, j, k)
                image_path = os.path.join(image_folder, name)
                if os.path.exists(image_path):
                    img = cv2.imread(image_path)
                    dst_name = "10_{}_{}_{}.jpg".format(i, j, k)
                    cv2.imwrite(os.path.join(dst_folder, dst_name), img)
    print('end')

def selectImage(image_folder = '/home/channy/Downloads/dataset_defect/1',
                dst_folder = '/home/channy/Downloads/dataset_class/class1/train',
                folderIdx = range(3, 11),
                firstIdx = range(1, 110),
                secondIdx = range(1, 2),
                lastIdx = [1, 4, 7, 10]):
    for fidx in folderIdx:
        for i in firstIdx:
            for j in secondIdx:
                for k in lastIdx:
                    name = "{}/{}_{}_{}.jpg".format(fidx, i, j, k)
                    image_path = os.path.join(image_folder, name)
                    if not os.path.exists(image_path):
                        break
                    img = cv2.imread(image_path)
                    # if (k & 1) == 1:
                    #     img = cv2.rotate(img, cv2.ROTATE_180)
                    if not os.path.exists(dst_folder):
                        os.mkdir(dst_folder)
                    dst_name = "{}_{}_{}_{}.jpg".format(fidx, i, j, k)
                    cv2.imwrite(os.path.join(dst_folder, dst_name), img)

def rotImage(in_folder = '/home/channy/Downloads/dataset_train/class2_8/test/bad/', out_folder = '/home/channy/Downloads/dataset_train/class2_8/test/bad/', in_name = '2_29_3_8_44.jpg'):
    img = cv2.imread(os.path.join(in_folder, in_name))
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite(os.path.join(out_folder, in_name), img)

# cv2.flip 0:up-down; 1:left-right
def flipImage(image_name = '/home/channy/Downloads/dataset_train/class2_8/test/bad/2_29_3_8_44.jpg'):
    out_name = image_name[:-4] + '_flip.jpg'
    image = cv2.imread(image_name)
    # image = cv2.rotate(image, cv2.ROTATE_180)
    image = cv2.flip(image, 1)
    cv2.imwrite(out_name, image)

def resizeToFixSize():
    image_folder = '/home/channy/Downloads/dataset_train/class1_1/test/bad/'
    image_list = os.listdir(image_folder)
    for i, image_name in enumerate(image_list):
        print('infer {} / {}'.format(i+1, len(image_list)), end='\r')
        image_path = os.path.join(image_folder, image_name)
        origin_image = cv2.imread(image_path)
        if origin_image.shape[1] == 1400:
            continue
        if origin_image.shape[0] == 1024:
            continue

        image = cv2.resize(origin_image, (1400, 1024))
        cv2.imwrite(os.path.join(image_folder, image_name), image)

def rgb2gray(img_folder, img_name):
    img_full_name = os.path.join(img_folder, img_name)
    image = cv2.imread(img_full_name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    target_color = np.array([255, 0, 0])
    mask = np.all(image == target_color, axis=-1).astype(np.uint8) * 255
    img_write_name = img_full_name + '.jpg'
    cv2.imwrite(img_write_name, mask)

if __name__ == '__main__':
    # resizeFolder()

    # selectImage(image_folder = '/home/channy/Downloads/dataset_defect/',
    #             dst_folder = '/home/channy/Downloads/dataset_train/class1_1/test/good',
    #             folderIdx = range(1, 3),
    #             firstIdx = range(1, 110),
    #             secondIdx = range(1, 2),
    #             lastIdx = [1])
    
    # for i in range(1, 9):
    #     for j in range(1, 22):
    #         selectImage(image_folder = '/home/channy/Downloads/dataset_defect',
    #                     dst_folder = '/home/channy/Downloads/dataset_class/val/class' + str(i) + '_' + str(j),
    #                     folderIdx = range(1, 3),
    #                     firstIdx = range(1, 110),
    #                     secondIdx = range(i, i + 1),
    #                     lastIdx = [j])

    # rotImage()

    flipImage()

    # resizeToFixSize()

    # img_folder = ''
    # image_list = os.listdir(img_folder)
    # for img_name in image_list:
    #     rgb2gray(img_folder, img_name)
    # rgb2gray()
    