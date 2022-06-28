# pdfdo
具备pdf文件
1. 剪切，
2. 旋转，
3. 合并，
4. 拆分，
5. 添加页码：将页码文档page-number.pdf放在软件同一目录下，
6. 转图片。
等功能。


# 相关库
1. pdf文档处理： PyPDF2.
2. pdf转图片: pdf2image.
3. word转pdf: pywin32, 调用Office.
4. UI：wxpython.
5. exe文件：pyinstaller.


# 打包方法
python需要3.6版本
首先安装上述库，其中pyinstaller可以官网下载压缩包，然后把待打包程序放在其解压文件夹下，然后命令行运行
pyinstaller -F -w xx/xx/app.py
其中-F, -w分别表示打包为单个执行exe程序，不显示命令行窗口。



@author JMx
date 2018-04-26
pdf文件拆分,合并,剪切等功能.

        1   将pdf文件拆分成单页.
            split_pdf_each(infn):                        
                    "infn"表示文件名(含路径).
                    例:split_pdf_each('F:/pdf/test.pdf').

        2   将pdf文件拆分成多个部分.
            split_pdf_parts(infn, parts): 
                    "infn"为文件名(含路径).
                    "parts"为每个部分起始页码列表.
                    例:split_pdf_parts('F:/p/1.pdf',[(1,3),(40,50)]).

        3   将多个pdf文件合并成一个.
            merge_pdf(infnList, outfn):                       
                    "infnList"为要合并的文件名(含路径)列表.
                    "outfn"为合并后文件名(含路径).
                    例:merge_pdf(['F:/1.pdf','F:/2.pdf'], 'F:/12.pdf').
                    
        4   将pdf文件页面剪切至合适大小.
            cut_pdf(infn, left, right, lower, upper, option, isTest):        
                    "infn"表示文件名(含路径).
                    2~5四个参数分别是四周需要剪去的宽度(一般在10～160).
                    "option"为剪切方式,all/odd/even 页.
                    "isTest"表示是否先对第一页进行测试.
                    例:cut_pdf('F:/1.pdf',20,20,20,20,'even',1).测试.
                                只剪切前两页,单独生成一个pdf文件.
                        cut_pdf('F:/1.pdf',20,20,20,20,'odd',0)不测试.
                                剪切奇数页.

