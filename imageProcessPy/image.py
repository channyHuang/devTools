import cv2
import numpy as np

def getGPS():
    from exif import Image
    for i in range(149, 323):
        with open('/home/channy/Documents/datasets_recon/dolphin_wall/images/DJI_0' + str(i) + '.JPG', 'rb') as f:
            img = Image(f)
            print(i, img.gps_latitude, img.gps_longitude)

def stitcher():
    
    # 读取两张部分重叠区域的图像
    img1 = cv2.imread('/home/channy/Documents/projects/OsgObjects/build/tmp/146.jpg')
    img2 = cv2.imread('/home/channy/Documents/projects/OsgObjects/build/tmp/155.jpg')

    # 使用 OpenCV 的 Stitcher 进行拼接和对齐
    stitcher = cv2.Stitcher_create(cv2.STITCHER_SCANS)
    status, result = stitcher.stitch([img1, img2])

    if status == cv2.STITCHER_OK:
        # 调整亮度和对比度
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # 计算曝光差异
        _, th1 = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        _, th2 = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # 调整亮度
        img1_adjusted = cv2.copyTo(img1, None, (th1 * 2.5).astype(np.float32))
        img2_adjusted = cv2.copyTo(img2, None, (th2 * 2.5).astype(np.float32))

        # 合并图像
        merged = np.where(th1[:, :, None], img1_adjusted, img2_adjusted)
        
        cv2.imwrite('merged_image.jpg', merged)
    else:
        print("Image stitching failed.")

def test():
    # 加载图像并转为RGB格式
    img1 = cv2.imread('/home/channy/Documents/datasets_recon/lightAdjust/146.jpg')
    img2 = cv2.imread('/home/channy/Documents/datasets_recon/lightAdjust/155.jpg')


    # 转换到HSV颜色空间
    hsv_ref = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    hsv_tar = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

    # 提取色调和饱和度通道
    ref_hue = hsv_ref[:, :, 0]
    ref_sat = hsv_ref[:, :, 1]

    tar_hue = hsv_tar[:, :, 0]
    tar_sat = hsv_tar[:, :, 1]

    # 创建CLAEH对象并应用到目标图像的色调和饱和度通道
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(3, 3))
    corrected_hue = clahe.apply(tar_hue)
    corrected_sat = clahe.apply(tar_sat)

    hue2 = clahe.apply(ref_hue)
    sat2 = clahe.apply(ref_sat)

    # 重新组合并转换回BGR颜色空间
    hsv_corrected1 = cv2.merge([corrected_hue, corrected_sat, hsv_tar[:, :, 2]])
    hsv_corrected2 = cv2.merge([hue2, sat2, hsv_ref[:, :, 2]])
    img_corrected1 = cv2.cvtColor(hsv_corrected1, cv2.COLOR_HSV2BGR)
    img_corrected2 = cv2.cvtColor(hsv_corrected2, cv2.COLOR_HSV2BGR)
    
    # cv2.imwrite('corrected_image.jpg', img_corrected)

    cv2.imshow('r1', img_corrected1)
    cv2.imshow('r2', img_corrected2)
    cv2.waitKey(10000)

def color():
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt

    # 读取图像
    reference_image = cv2.imread('/home/channy/Documents/datasets_recon/lightAdjust/146.jpg')
    input_image = cv2.imread('/home/channy/Documents/datasets_recon/lightAdjust/155.jpg')

    # 特征检测和匹配（SIFT + BFMatcher）
    sift = cv2.SIFT_create()
    kp_ref, des_ref = sift.detectAndCompute(reference_image, None)
    kp_input, des_input = sift.detectAndCompute(input_image, None)

    bf = cv2.BFMatcher()
    matches = bf.match(des_ref, des_input)
    # matches.sort(key=lambda x: x.distance)
    # Assuming matches is a list of match objects (e.g., cv2.DMatch)
    # Convert matches to a list if it's not already one
    matches_list = list(matches)

    # Sort indices based on the distance in the matches
    indices = range(len(matches_list))
    sorted_indices = sorted(indices, key=lambda i: matches_list[i].distance)

    # Create a new list of matches sorted by distance
    sorted_matches = [matches_list[i] for i in sorted_indices]

    good_matches = sorted_matches[:100]

    # 计算Homography变换
    points_ref = np.array([kp_ref[m.queryIdx].pt for m in good_matches], dtype=np.float32)
    points_input = np.array([kp_input[m.trainIdx].pt for m in good_matches], dtype=np.float32)

    H, _ = cv2.findHomography(points_input, points_ref, method=cv2.FM_RANSAC, 
    ransacReprojThreshold=5.0)

    # 应用变换
    affine_part = H[:2, :3]  # 取前两行前三列，得到一个2x3的矩阵
    H = affine_part.astype(np.float32)
    registered_image = cv2.warpAffine(input_image, H, (reference_image.shape[1], 
    reference_image.shape[0]))

    # 转换为HSV颜色空间
    hsv_ref = cv2.cvtColor(reference_image, cv2.COLOR_RGB2HSV)
    hsv_registered = cv2.cvtColor(registered_image, cv2.COLOR_RGB2HSV)

    # 提取通道
    h_ref, s_ref, v_ref = cv2.split(hsv_ref)
    h_reg, s_reg, v_reg = cv2.split(hsv_registered)

    # 使用CLAHE进行颜色校正
    clahe = cv2.createCLAHE(clipLimit=0.01, tileGridSize=(8,8))

    h_ref_equalized = clahe.apply(h_ref)
    s_ref_equalized = clahe.apply(s_ref)
    v_ref_equalized = clahe.apply(v_ref)

    # 合并调整后的HSV通道
    hsv_adjusted = cv2.merge([h_ref_equalized, s_ref_equalized, v_ref_equalized])
    adjusted_image = cv2.cvtColor(hsv_adjusted, cv2.COLOR_HSV2RGB)

    # 显示图像
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1), plt.imshow(reference_image), plt.title('Reference Image')
    plt.subplot(1, 3, 2), plt.imshow(registered_image), plt.title('Registered Image')
    plt.subplot(1, 3, 3), plt.imshow(adjusted_image), plt.title('Adjusted Image')
    plt.show()

if __name__ == '__main__':
    # getGPS()
    # stitcher()
    # test()
    img1 = cv2.imread('/home/channy/Documents/datasets_recon/lightAdjust/146.jpg')
    color()
