from PyPDF2 import PdfFileReader, PdfFileWriter
import sys
import os
import fitz

class PDF: 
    def __init__(self):
        self.infn = []
        self.params = ''
        self.message = ''

    def pdf_info(self):
        return [ 'ID:%d, 页数:%d, 宽×高:%d×%d  ' % (i+1, p.getNumPages(), p.getPage(0).mediaBox.upperRight[0], p.getPage(0).mediaBox.upperRight[1]) for i, p in enumerate( [ PdfFileReader( open(p, 'rb') ) for p in self.infn ] ) ]


    def split_pdf_each(self): 
        for infn in self.infn:
            try:
                pdf_name = infn.split('\\')[-1];
                dir_ = infn.replace(pdf_name, pdf_name[:-4] + '\\')
                if not os.path.exists(dir_):
                    os.mkdir(dir_)
                pdf_input = PdfFileReader(open(infn, 'rb')) 
                pages = pdf_input.getNumPages()  
                self.message = '正在拆分...'
                for i in range(pages): 
                    pdf_output = PdfFileWriter()
                    pdf_output.addPage(pdf_input.getPage(i)) 
                    pdf_output.write(open(dir_ + pdf_name[:-4] + '-' + str(i + 1) + '.pdf', 'wb')) 
                    self.message = pdf_name + ':  ' + str(i) + '/' + str(pages)
            except:
                self.message = '出错了，请检查输入格式是否正确'
        self.message = '完成'

    def split_pdf_parts(self): 
        for infn in self.infn:
            try:
                pdf_input = PdfFileReader(open(infn, 'rb'))
                self.message = '正在拆分...'
                for part in self.params:
                    pdf_output = PdfFileWriter()
                    for i in range(part[0] - 1, part[1]):
                        pdf_output.addPage(pdf_input.getPage(i));
                    pdf_output.write(open(infn[:-4] + '-' + str(part[0]) + '-' + str(part[1]) + '.pdf', 'wb'))
                    self.message = '第%d部分已拆分'%(self.params.index(part) + 1)
            except:
                self.message = '出错了，请检查输入格式是否正确'
        self.message = '完成'

    def merge_pdf(self): 
        try:
            pdf_output = PdfFileWriter() 
            self.message = '正在合并...'
            for infn in self.infn:
                self.message = infn
                pdf_name = infn.split('\\')[-1];
                pdf_input = PdfFileReader(open(infn, 'rb')) 
                pages = pdf_input.getNumPages() 
                for i in range(pages): 
                    pdf_output.addPage(pdf_input.getPage(i)) 
                    self.message = pdf_name + ':  ' + str(i) + '/' + str(pages)
            pdf_output.write(open(self.params, 'wb')) 
            self.message = '合并完成，合并文件位于第一个文件所在地'
        except:
            self.message = '出错了，请检查输入格式是否正确'

    def cut_pdf(self):
        try:
            left, right, lower, upper, option, isTest = self.params;
            self.message = '正在剪切'
            pdf_name = self.infn[0].split('\\')[-1];
            pdf_input = PdfFileReader(open(self.infn[0], 'rb'));
            pdf_output = PdfFileWriter();
            pages = pdf_input.getNumPages()
            if isTest == 1:
                pages = min(10 * isTest, pages)
            for i in range(pages):
                page = pdf_input.getPage(i);
                if (option == 'all') or (option == 'odd' and i%2 == 0) or (option == 'even' and (i+1)%2 == 0):
                    page.mediaBox.upperLeft = (left, page.mediaBox.upperLeft[1] - upper)
                    page.mediaBox.upperRight = (page.mediaBox.upperRight[0] - right, page.mediaBox.upperRight[1] - upper)
                    page.mediaBox.lowerLeft = (left, lower)
                    page.mediaBox.lowerRight = (page.mediaBox.lowerRight[0] - right, lower)
                pdf_output.addPage(page);
                self.message = pdf_name + ':  ' + str(i) + '/' + str(pages)  
            pdf_output.write(open(self.infn[0][:-4] + '-cut.pdf', 'wb'));
            self.message = '剪切完成'
        except:
            self.message = '出错了，请检查输入格式是否正确'

    def rotate_pdf(self):
        try:
            pdf_name = self.infn[0].split('\\')[-1];
            rotation, isTest = self.params
            self.message = '正在旋转'
            pdf_input = PdfFileReader(open(self.infn[0], 'rb'));
            pdf_output = PdfFileWriter();
            pages = isTest or pdf_input.getNumPages();
            for i in range(pages):
                page = pdf_input.getPage(i);
                page.rotateClockwise(rotation);
                pdf_output.addPage(page);
                self.message = pdf_name + ':  ' + str(i) + '/' + str(pages)                
            pdf_output.write(open(self.infn[0][:-4] + '-rotate.pdf', 'wb'));
            self.message = '完成旋转'
        except:
            self.message = '出错了，请检查输入格式是否正确(旋转角度为90的倍数)'

    def add_watermark(self):
        self.message = '正在添加页码'
        water_pdf = PdfFileReader(open('page-number.pdf', 'rb'));
        water_pages = water_pdf.getNumPages()
        for infn in self.infn:
            try:
                pdf_name = infn.split('\\')[-1];
                pdf_input = PdfFileReader(open(infn, 'rb'));
                pages = min(pdf_input.getNumPages(), water_pages);
                pdf_output = PdfFileWriter();
                for i in range(pages):
                    page = pdf_input.getPage(i);
                    water_page = water_pdf.getPage(i);
                    page.mergePage(water_page);
                    pdf_output.addPage(page);
                    self.message = pdf_name + ':  ' + str(i) + '/' + str(pages)
                pdf_output.write(open(infn[:-4] + '-number2.pdf', 'wb'));
            except: 
                self.message = '出错了，请检查输入格式是否正确(page-number.pdf文件要求和程序在同一目录)'
        self.message = '完成';

    def convert_pdf2_image(self):
        self.message = '正在转换，所需时间较长，请稍等'
        zoom, type_ = self.params
        for infn in self.infn:
            try:
                pdf_name = infn.split('\\')[-1];
                dir_ = infn.replace(pdf_name, pdf_name[:-4] + '\\')
                if not os.path.exists(dir_):
                    os.mkdir(dir_)
                doc = fitz.open(infn)
                for pg in range(doc.pageCount):
                    page = doc[pg]
                    rotate = int(0)
                    trans = fitz.Matrix(zoom, zoom).preRotate(rotate)
                    pm = page.getPixmap(matrix=trans, alpha=False)
                    pm.writePNG( dir_ + pdf_name + '-' + str(pg) + '.' + type_ ) 
                    self.message = pdf_name + ':  ' + str(pg + 1) + '/' + str(doc.pageCount) ;
            except:
                self.message = '出错了，请检查输入格式是否正确'
        self.message = '完成';