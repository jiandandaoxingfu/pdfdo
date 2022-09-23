# pdfdo
具备pdf文件
1. 剪切，
2. 旋转，
3. 合并，
4. 拆分，
5. 添加页码：将页码文档page-number.pdf放在软件同一目录下，
6. 转图片。
7. word转pdf(需要安装word)
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
