# -*- coding: utf-8 -*-
# @Time    : 2022/5/22 20:58
# @Author  : xiaosong
# @File    : image_enAndDecription.py
# @Software: PyCharm
import os, re

import numpy as np
import cv2


def image_en(filePath):
    '''
    :param filePath: 文件路径
    :return: 无
    图片格式必须为无损的格式，否则加解密过后会失真
    '''
    global key
    path, name = os.path.split(filePath)
    keyFileName = re.split('\.', name)[0]
    img = cv2.imread(filePath, -1)
    width, height, deep = img.shape
    # 密钥文件路径
    keyPath = os.path.join(path, keyFileName + ".npy")
    if os.path.exists(keyPath):
        key = np.load(keyPath)
    else:
        key = np.random.randint(0, 256, size=[width, height, deep], dtype=np.uint8)
        # 保存密钥
        np.save(keyPath, key)

    encryption = cv2.bitwise_xor(img, key)
    cv2.imwrite(filePath, encryption)


    # 显示预览图片
    # cv2.imshow("111", encryption)
    # cv2.waitKey()
    # cv2.destroyAllWindows()


def image_de(filePath):
    global key
    path, name = os.path.split(filePath)
    keyFileName = re.split('\.', name)[0]
    # 密钥文件
    keyPath = os.path.join(path, keyFileName + ".npy")
    img = cv2.imread(filePath, -1)
    width, height, deep = img.shape

    if os.path.exists(keyPath):
        key = np.load(keyPath)
    else:
        key = np.random.randint(0, 256, size=[width, height, deep], dtype=np.uint8)
        # 保存密钥
        np.save(keyPath, key)

    decryption = cv2.bitwise_xor(img, key)

    cv2.imwrite(filePath, decryption)

    # cv2.imshow("111", encryption)
    cv2.imshow("222", decryption)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    filePath = "E:\\MyProject\\pythonproject\Django\\target_djangoProject1\\media\\hongsong\\IMG_20220406_111401.png"
    # image_en(filePath)
    # image_de(filePath)
    print("结束")

