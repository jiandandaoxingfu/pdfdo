import wx, time
from PDF import PDF
from threading import Thread

# Next, create an application object.
app = wx.App()

# Then a frame.
frm = wx.Frame(None, title="pdf处理器", pos = (600, 300), size = (500, 400));

fn = ''
path = ''
def select_files():
	if fileDialog.ShowModal() == wx.ID_OK:
		global fn, path
		wx.FindWindowById(0).SetValue(str(fileDialog.GetFilenames()))
		path = fileDialog.GetDirectory()
		fn = [path + '\\' + f for f in fileDialog.GetFilenames()]
		pdfdo.infn = fn
		message.SetValue(str(pdfdo.pdf_info()))

# component

def btn_callback(event):
	id_ = event.GetId()

	if id_ == 1:
		select_files()
		return

	if fn == '':
		return

	pdfdo.message = ''
	param_ = wx.FindWindowById(id_ - 1).GetValue()
	param = []
	if (id_ != 3) & (id_ != 7) & (id_ != 13):
		try:
			param = eval(param_)
		except:
			message.SetValue('输入格式有误')
			return

	Thread(target = update_state).start()	

	pdfdo.params = param;

	if id_ == 3:
		Thread(target = pdfdo.split_pdf_each).start()
	elif id_ == 5:
		Thread(target = pdfdo.split_pdf_parts).start()
	elif id_ == 7:
		pdfdo.params = path + '\\' + param_
		Thread(target = pdfdo.merge_pdf).start()
	elif id_ == 9:
		Thread(target = pdfdo.cut_pdf).start()
	elif id_ == 11:
		Thread(target = pdfdo.rotate_pdf).start()
	elif id_ == 13:
		Thread(target = pdfdo.add_watermark).start()
	elif id_ == 15:
		Thread(target = pdfdo.convert_pdf2_image).start()
	

def update_state():
	message.SetValue(pdfdo.message)
	if ('完成' not in pdfdo.message) & ('出错了' not in pdfdo.message):
		time.sleep(1)
		update_state()
	else:
		message.SetValue(pdfdo.message)

# select file
fileDialog = wx.FileDialog(frm, message = '选择文件', wildcard = '*.pdf', style = wx.FD_OPEN | wx.FD_MULTIPLE, pos = (200, 30), size = (100, 25))

# input/button: pos = (left, top), size = (width, height).
# varibles.
left = 15;
width = 390;
top = 20;
margin = 36;
labels = ['选择文件', '拆分每页', '部分拆分', '文件合并', '文件剪切', '文件旋转', '添加页码', '转为图片'];
default_values = ['支持拖入文件', '支持多个文件', '支持多个文件， 如：[(1,3),(20,25),(30,40)]', '合并后文件名.pdf', '支持单个文件，如：[10,20,10,20,"even",1] (注：左, 右, 下, 上, odd/even/all, 0/1: 0为全部, 1为测试10张)', '支持单个文件，如：[90,1] (注：旋转度数是90的整数倍, 0/1: 1为测试一张, 0为全部)', '支持多个文件', '支持多个文件： 如[5,"png"], 数值越大，图片越清晰，转换也越慢']
length = len(labels)

for i in range(length):
	wx.TextCtrl(frm, id = 2 * i, value = default_values[i], pos = (left, top + margin * i), size = (width, 25));
	wx.Button(frm, id = 2 * i + 1, label = labels[i], pos = (width + 20, top + margin * i), size = (60, 25)).Bind(wx.EVT_BUTTON, btn_callback);

message = wx.TextCtrl(frm, value = "状态框", pos = (left, top + margin * length + 5), size = (455, 25))

# drop
class FileDrop(wx.FileDropTarget):

	def __init__(self, window):
		wx.FileDropTarget.__init__(self)
		self.window = window
		
	def OnDropFiles(self, x, y, filenames):
		global fn, path
		fn = [f.replace('\\', '\\\\') for f in filenames]
		pdfdo.infn += fn
		length = len(pdfdo.infn[0].split('\\')[-1])
		path = pdfdo.infn[0][0:-length-2]
		print(path)
		message.SetValue(str(pdfdo.pdf_info()))
		fn_ = [f.split("\\")[-1] for f in pdfdo.infn]
		wx.FindWindowById(0).SetValue(str(fn_));
		return True

drop2 = FileDrop(wx.FindWindowById(0));
wx.FindWindowById(0).SetDropTarget(drop2);

pdfdo = PDF()

# Show it.
frm.Show()

# Start the event loop.
app.MainLoop()
