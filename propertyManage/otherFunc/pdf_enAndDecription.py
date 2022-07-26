# -*- coding: utf-8 -*-
# @Time    : 2022/5/22 20:46
# @Author  : xiaosong
# @File    : pdf_enAndDecription.py
# @Software: PyCharm
from PyPDF2 import PdfFileWriter, PdfFileReader


def PDF_en(filePath, password):
    pdf_reader = PdfFileReader(filePath)  # 输入你想要操作的pdf文档的位置/名称
    pdf_writer = PdfFileWriter()

    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))

    pdf_writer.encrypt(password)  # 括号里面填写密码
    with open(filePath, 'wb') as out:
        pdf_writer.write(out)


def PDF_de(filePath, password):
    pdf_reader = PdfFileReader(filePath)  # 输入你想要操作的pdf加密的文档的位置/名称
    pdf_reader.decrypt(password)
    pdf_writer = PdfFileWriter()

    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))

    with open(filePath, 'wb') as out:
        pdf_writer.write(out)


if __name__ == '__main__':
    filePath = "E:\\MyProject\\pythonproject\Django\\target_djangoProject1\\media\\hongsong\\成都理工大学计网牛关于毕业论文形式规范检测的通知.pdf"
    # PDF_en(filePath, "123456")
