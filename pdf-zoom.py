import sys
import os

from pdfrw import PdfReader, PdfWriter, PageMerge, IndirectPdfDict


def adjust(page, margin=0, scale=1):
    info = PageMerge().add(page)
    x1, y1, x2, y2 = info.xobj_box
    viewrect = (margin, margin, x2 - x1 - 2 * margin, y2 - y1 - 2 * margin)
    page = PageMerge().add(page, viewrect=viewrect)
    page[0].scale(scale)
    return page.render()


inpfn = 'F:page-number.pdf'
outfn = 'F:poster.' + os.path.basename(inpfn)
reader = PdfReader(inpfn)
writer = PdfWriter(outfn)
writer.addpage(adjust(reader.pages[0]))
writer.trailer.Info = IndirectPdfDict(reader.Info or {})
writer.write()