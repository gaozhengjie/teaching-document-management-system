from django.http import HttpResponse
from django.shortcuts import render
from file_manage_app.models import File, Frequent_items


def preview(request):
    query_file_name = request.GET.get("file_name")
    # html_path = 'cache\\' + query_file_name[:(query_file_name.index('.'))] + '.html'
    html_path = File.objects.filter(file_name=query_file_name)[0].preview_file_path
    file_id = File.objects.filter(file_name=query_file_name)[0].file_id
    relevant_list = Frequent_items.objects.filter(main_file_id=file_id).values_list('relevant_file_id')
    relevant_filename = []
    for i in relevant_list:
        relevant_filename.append(File.objects.filter(file_id=i[0])[0].file_name)
    return render(request, "preview.html", locals())
