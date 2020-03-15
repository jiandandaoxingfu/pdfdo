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