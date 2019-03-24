from django.http import HttpResponse
from django.views.decorators import csrf
from django.shortcuts import render
from file_manage_app.models import File, Keyword, Rec
import numpy as np

def index(request):
    file_list = File.objects.all().order_by('-file_id')  # 按照时间顺序排列，最新上传的文件排在最上面
    keyword_list = Keyword.objects.all()
    user_id = np.random.randint(0, 12)
    rec_list = Rec.objects.filter(user_id=user_id).values_list('rec_file_id')
    rec_filename = []
    for i in rec_list:
        rec_filename.append(File.objects.filter(file_id=i[0])[0].file_name)
    return render(request, "index.html", locals())

def filter_file_type(request):
    file_list = File.objects.filter(file_type=request.GET.get('file_type'))
    keyword_list = Keyword.objects.all()
    user_id = np.random.randint(0, 12)
    rec_list = Rec.objects.filter(user_id=user_id).values_list('rec_file_id')
    rec_filename = []
    for i in rec_list:
        rec_filename.append(File.objects.filter(file_id=i[0])[0].file_name)
    return render(request, "index.html", locals())