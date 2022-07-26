# -*- coding: utf-8 -*-
# @Time    : 2022/5/22 20:15
# @Author  : xiaosong
# @File    : judgeFileTypeAndOperate.py
# @Software: PyCharm
from .image_enAndDecription import *
from .officeFileAddPD import *
from .txt_encryptAndDecode import *
from .pdf_enAndDecription import *


def judgeFileType(opFilePath, password=None, fileType=None, opType=1):
    if opType == 1:
        if (fileType == 'image/jpeg') or (fileType == 'image/png'):
            image_en(opFilePath)
        elif fileType == 'application/pdf':
            PDF_en(opFilePath, password)
        elif fileType == 'application/zip':
            officeEncryption(opFilePath, password)
        elif fileType == '.txt':
            txt_encrypt(opFilePath, password)
        elif fileType == '.html':
            pass
        else:
            pass
    else:
        if (fileType == 'image/jpeg') or (fileType == 'image/png'):
            image_de(opFilePath)
        elif fileType == 'application/pdf':
            PDF_de(opFilePath, password)
        elif fileType == 'application/zip':
            officeDecryption(opFilePath, password)
        elif fileType == '.txt':
            txt_decrypt(opFilePath, password)
        elif fileType == '.html':
            pass
        else:
            pass
