from win32com import client as wc
import os
import pythoncom


def doc2html(filename, absolute_path):
    pythoncom.CoInitialize()
    wd = wc.Dispatch('Word.Application')
    doc = wd.Documents.Open(absolute_path)
    doc.SaveAs(os.getcwd() + '\\file_manage_app\\static\\cache\\' + filename + '.html', 8)  # 8的值对应HTML
    doc.Close()
    wd.Quit()


def xls2html(filename, absolute_path):
    pythoncom.CoInitialize()
    ex = wc.Dispatch('Excel.Application')
    xls = ex.Workbooks.Open(absolute_path)
    xls.SaveAs(os.getcwd() + '\\file_manage_app\\static\\cache\\' + filename + '.html', 44)  # 44的值对应HTML
    xls.Close()
    ex.Quit()
