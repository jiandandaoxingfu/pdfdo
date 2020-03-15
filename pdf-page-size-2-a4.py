# -*- coding: utf-8 -*-
# @Author:	        old jia
# @Email:              jiaminxin@outlook.com
# @Date:               2019-08-22 13:25:39
# @Last Modified by:   old jia
# @Last Modified time: 2019-08-23 23:04:33
import sys
from pdfrw import PdfReader, PdfWriter, PageMerge, IndirectPdfDict

def get_size(infn, i):
	pdf = PdfReader(infn)
	size = PageMerge().add(pdf.pages[i]).xobj_box;
	print(size)
	return (size[2], size[3])

def get_scale_margin(infn, a4_size, i):
	size = get_size(infn, i)
	width_ratio = a4_size[0] / size[0]
	height_ratio = a4_size[1] / size[1]
	scale = max(width_ratio, height_ratio)
	if width_ratio > height_ratio :
		margin = (size[1] * scale - a4_size[1]) / 2
		is_vertical = 1
	else:
		margin = (size[0] * scale- a4_size[0]) / 2
		is_vertical = 0
	return (scale, margin, is_vertical)

def adjust(page, params):
	scale, margin, is_vertical = params
	info = PageMerge().add(page)
	x1, y1, x2, y2 = info.xobj_box
	if is_vertical == 1:
		viewrect = (0, margin / scale, x2, y2 - 2 * margin / scale)
	else:
		viewrect = (margin / scale, 0, x2 - 2 * margin / scale, y2)
	page = PageMerge().add(page, viewrect=viewrect)
	page[0].scale(scale)
	return page.render()

def resize_2_a4(infn):
	outfn = infn[:-4] + '-A4.pdf';
	reader = PdfReader(infn)
	writer = PdfWriter(outfn)
	a4_size = get_size('A4.pdf', 0)
	params = get_scale_margin(infn, a4_size, 0)
	for page in reader.pages:
		writer.addpage(adjust(page, params))
	writer.trailer.Info = IndirectPdfDict(reader.Info or {})
	writer.write()

if __name__ == '__main__': 
	cmd = sys.argv[1].encode('gb2312').decode('gb2312');
	resize_2_a4(cmd);