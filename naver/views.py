from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .crawling import main
from .crawling import excelFunc
from django.core.files.storage import default_storage

# Create your views here.

def index(request):
    return render(request, 'naver/index.html')

def crawling(request):
    main.crawling(request.POST['url'])
    # main.crawling()
    # return "hi"
    return HttpResponseRedirect(reverse('index'))

def excel(request):
    excelFunc.db_to_xl()
    return HttpResponseRedirect(reverse('index'))

def fileUpload(request):
    for img in request.FILES.getlist('files'):
        path = default_storage.save('static/naver/img/' + str(img), img)
        print(path)
    return HttpResponseRedirect(reverse('index'))