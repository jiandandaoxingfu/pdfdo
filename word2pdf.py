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
            self.message = '开始转换, 请稍后'
            gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 4)
            # 开始转换
            w = Dispatch("Word.Application")
            for i in range(len(self.infn)):
                filename = self.infn[i]
                (filepath, filename) = os.path.split(filename)  
                softfilename = os.path.splitext(filename) 
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
                    self.message = str(i+1) + '/' + str(len(self.infn))
                except Exception as e:
                    print(e)
                if os.path.isfile(pdf_name):
                    valueList.append(pdf_name)
                else:
                    self.message = '出错:'
                    return False
            w.Quit(constants.wdDoNotSaveChanges)
            self.message = '完成'
            return valueList
        except TypeError as e:
            self.message = '出错'
            print(e)
            return False