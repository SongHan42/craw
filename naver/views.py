from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.template import loader
from .models import *

from .crawling import main
from .crawling import excelFunc
# from .crawling import shipping
from .models import Shipping
from django.core.files.storage import default_storage
import os
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, 'naver/index.html')

def crawling(request):
    result = main.crawling.delay(request.POST['url'])
    return render(request, 'naver/display_progress.html', context={'task_id': result.task_id})

def excel(request):
    excelFunc.db_to_xl()
    print(settings.STATIC_ROOT)
    file_path = os.path.join(settings.STATIC_ROOT, "test.xlsx")
    print(file_path)

    if os.path.exists(file_path):
        binary_file = open(file_path, 'rb')
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    return HttpResponseRedirect(reverse('index'))
