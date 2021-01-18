# pdfdo
具备pdf文件
1. 剪切，
2. 旋转，
3. 合并，
4. 拆分，
5. 添加页码：将页码文档page-number.pdf放在软件同一目录下。
等功能。


# 相关库
1. pdf文档处理： PyPDF2.
2. UI：wx.
3. exe文件：pyinstaller, pywin32, pywin32-ctypes.


# 打包方法
首先安装上述三个库，其中pyinstaller可以官网下载压缩包，然后把待打包程序放在其解压文件夹下，然后命令行运行
python pyinstaller.py -F -w client.py
其中-F, -w分别表示打包为单个执行exe程序，不显示命令行窗口。
