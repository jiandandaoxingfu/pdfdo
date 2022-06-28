# -*- coding:utf-8 -*-

import os
from win32com.client import Dispatch, DispatchEx
from win32com.client import constants
from win32com.client import gencache

# Word to PDF
class Word2PDF:
    def __init__(self):
        self.infn = []
        self.message = ''

    def run(self):
        valueList = []
        try:
            gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 4)
            # 开始转换
            w = Dispatch("Word.Application")
            for fullfilename in self.infn:
                (filepath, filename) = os.path.split(fullfilename)  # 分割文件路径和文件名
                softfilename = os.path.splitext(filename)  # 分割文件名和扩展名
                os.chdir(filepath)
                doc = os.path.abspath(filename)
                os.chdir(filepath)
                pdfname = softfilename[0] + ".pdf"
                output = os.path.abspath(pdfname)
                pdf_name = output
    
                try:
                    doc = w.Documents.Open(doc, ReadOnly=1)
                    doc.ExportAsFixedFormat(output, constants.wdExportFormatPDF,
                                    Item=constants.wdExportDocumentWithMarkup,
                                    CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
                except Exception as e:
                    print(e)
                if os.path.isfile(pdf_name):
                    valueList.append(pdf_name)
                else:
                    self.message = '转换失败！'
                    return False
            w.Quit(constants.wdDoNotSaveChanges)
            return valueList
        except TypeError as e:
            self.message = '出错了！'
            print(e)
            return False

word2pdf = Word2PDF()
word2pdf.infn = ["G:1.docx"];
word2pdf.run();