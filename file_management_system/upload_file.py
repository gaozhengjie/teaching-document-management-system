from django.http import HttpResponse
from django.shortcuts import render
import os
import math
from file_manage_app.models import File
from .extract_text import readPdf, readWord, readExcel
from .convert2html import doc2html, xls2html

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        path_file = BASE_DIR + "\\file_manage_app\\static\\upload"
        file_name = myFile.name
        local_url = os.path.join(path_file, file_name)
        if not os.path.isdir(path_file):
            os.mkdir(path_file)
        destination = open(local_url, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 存储到数据库，暂时只对TXT文本文件进行内容存储
        if file_name[-4:] == '.txt':
            with open(local_url, 'r', encoding='utf-8') as fp:
                file_text = fp.read()
                preview_file_path = "upload\\" + file_name
        elif file_name[-4:] == '.pdf':
            file_text = readPdf(local_url)
            preview_file_path = "upload\\" + file_name
        elif file_name[-4:] == '.doc' or file_name[-5:] == '.docx':
            file_text = readWord(local_url)
            doc2html(file_name, local_url)  # 注意是绝对路径
            preview_file_path = "cache\\" + file_name + '.html'
        elif file_name[-4:] == '.xls' or file_name[-5:] == '.xlsx':
            file_text = readExcel(local_url)
            xls2html(file_name, local_url)
            preview_file_path = "cache\\" + file_name + '.html'
        else:
            file_text = ''
            preview_file_path = ''

        # 换算文件大小的单位
        lst = ['B', 'KB', 'MB', 'GB']
        bytes = myFile.size
        i = int(math.floor(math.log(int(bytes), 1024)))
        if i >= len(lst):
            i = len(lst) - 1
        file_size = ('%.2f' + " " + lst[i]) % (bytes / math.pow(1024, i))

        File.objects.create(
            file_name=file_name,
            file_text=file_text,
            local_url="upload\\" + file_name,
            file_size=file_size,
            preview_file_path=preview_file_path,
            file_type=request.POST['file_type']
        )

        file_list = File.objects.all().order_by('-file_id')  # 逆序排列

        # return HttpResponse("upload over!")
        return render(request, "index.html", locals())