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

            try:
                gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 4)
                w = Dispatch("Word.Application")
            except:
                self.message = '电脑上可能没有安装Office, 无法使用'
                return

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
                except:
                    self.message = '出错了(1): ' + filename + '  转换失败'
                    return
                if os.path.isfile(pdf_name):
                    valueList.append(pdf_name)
                else:
                    self.message = '出错了(2): ' + filename + '  转换失败'
                    return
            w.Quit(constants.wdDoNotSaveChanges)
            self.message = '完成'
            return valueList
        except:
            self.message = '出错了, 已停止转换'
            return

if __name__=='__main__':
    w2p = Word2PDF()
    w2p.infn = ['F:1.docx', 'F:2.doc']
    w2p.run()
    print(w2p.message)