from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .crawing import main
from .crawing import excelFunc

# Create your views here.

def index(request):
    return render(request, 'naver/index.html')

def crawing(request):
    main.crawing(request.POST['url'])
    # main.crawing()
    # return "hi"
    return HttpResponseRedirect(reverse('index'))

def excel(request):
    excelFunc.db_to_xl()
    return HttpResponseRedirect(reverse('index'))