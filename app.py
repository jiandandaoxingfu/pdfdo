import wx, time, re, os
import webbrowser
from PDF import PDF
from word2pdf import Word2PDF
from threading import Thread

pdfdo = PDF()
word2pdf = Word2PDF()

app = wx.App()
frm = wx.Frame(None, title="pdf处理器", size = (600, 470));
message = False

def split_fn(fn):
	word2pdf.infn += list( filter(lambda f: os.path.splitext(f)[1] in ['.doc', '.docx'] , fn) )
	pdfdo.infn += list( filter(lambda f: os.path.splitext(f)[1] == '.pdf' , fn) )
	message.SetValue('PDF文档信息: ' + str(pdfdo.pdf_info()) )
	fn = [f.split("\\")[-1] for f in (word2pdf.infn + pdfdo.infn)]
	wx.FindWindowById(0).SetValue(str(fn));

def select_files():
	if fileDialog.ShowModal() == wx.ID_OK:
		path = fileDialog.GetDirectory()
		fn = fileDialog.GetFilenames()
		print(fn)
		split_fn(fn)

def update_state():
	message.SetValue(pdfdo.message or word2pdf.message)
	message2 = pdfdo.message + word2pdf.message
	if ('完成' not in message2) and ('出错' not in message2):
		time.sleep(1)
		update_state()
	elif message2:
		message.SetValue(pdfdo.message or word2pdf.message)
	pdfdo.message = ''
	word2pdf.message = ''
		
def btn_callback(event):
	id_ = event.GetId()

	if id_ == 1:
		select_files()
		return
	if ( not(pdfdo.infn) and (id_ in list(range(1, 17, 2))) ) or ( not(word2pdf.infn) and id_ == 17 ):
		message.SetValue('请选择文件')
		return

	pdfdo.message = ''
	param_ = wx.FindWindowById(id_ - 1).GetValue()
	param = []
	if id_ not in [3, 7, 13, 17, 19]:
		try:
			param = eval(param_)
		except:
			message.SetValue('输入格式有误')
			return

	Thread(target = update_state).start()	

	pdfdo.params = param;

	if id_ == 3:
		pdfdo.split_pdf_each()
	elif id_ == 5:
		pdfdo.split_pdf_parts()
	elif id_ == 7:
		(path, filename) = os.path.split(pdfdo.infn[0])
		merge_fn = wx.FindWindowById(6).GetValue() or '合并文件.pdf';
		pdfdo.params = path + '\\' + merge_fn
		pdfdo.merge_pdf()
	elif id_ == 9:
		pdfdo.cut_pdf()
	elif id_ == 11:
		pdfdo.rotate_pdf()
	elif id_ == 13:
		pdfdo.add_watermark()
	elif id_ == 15:
		pdfdo.pdf2image()
	elif id_ == 17:
		word2pdf.run()
	elif id_ == 19:
		webbrowser.open('https://github.com/jiandandaoxingfu/pdfdo')

def create_gui():
	# input/button: pos = (left, top), size = (width, height).
	left = 15
	width = 450
	top = 20
	margin = 40
	height = 30
	labels = ['选择文件', '拆分每页', '部分拆分', '文件合并', '文件剪切', '文件旋转', '添加页码', '转为图片', 'Word转PDF', '使用说明']
	default_values = [
	 '支持拖入文件',
	 '支持多个文件',
	 '支持多个文件，如：[(1,3),(20,25),(30,40)]',
	 '合并后文件名.pdf',
	 '支持单个文件，如：[10,20,10,20,"even",1] (注：左, 右, 下, 上, odd/even/all, 0/1: 0为全部, 1为测试10张)',
	 '支持单个文件，如：[90,1] (注：旋转度数是90的整数倍, 0/1: 1为测试一张, 0为全部)',
	 '支持多个文件', 
	 '支持多个文件, 如: 200, 数值越大，图片越清晰，转换也越慢', 
	 '支持多个文件(电脑需要安装有 Microsoft Word)',
	 '状态框'
	 ]
	length = len(labels)
		
	fileDialog = wx.FileDialog(frm, message = '选择文件', wildcard = '*.pdf;*.doc;*.docx', style = wx.FD_OPEN | wx.FD_MULTIPLE, pos = (200, 30), size = (100, 25))	

	for i in range(length):
		wx.TextCtrl(frm, id = 2 * i, value = default_values[i], pos = (left, top + margin * i), size = (width, height))
		wx.Button(frm, id = 2 * i + 1, label = labels[i], pos = (width + 20, top + margin * i), size = (100, height)).Bind(wx.EVT_BUTTON, btn_callback)	

	# message = wx.TextCtrl(frm, value = "状态框", pos = (left, top + margin * length + 5), size = (555, height))
	return (fileDialog, wx.FindWindowById(length * 2 - 2))

class FileDrop(wx.FileDropTarget):

	def __init__(self, window):
		wx.FileDropTarget.__init__(self)
		self.window = window
		
	def OnDropFiles(self, x, y, fn):
		fn = [f.replace('\\', '\\\\') for f in fn]
		split_fn(fn)
		return True

(fileDialog, message) = create_gui()
drop = FileDrop(wx.FindWindowById(0));
wx.FindWindowById(0).SetDropTarget(drop);

frm.Center()
frm.Show()
app.MainLoop()




