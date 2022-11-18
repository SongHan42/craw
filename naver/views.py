from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .crawling import main
from .crawling import excelFunc

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