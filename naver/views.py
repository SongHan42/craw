from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .crawling import main
from .crawling import excelFunc
# from .crawling import shipping
from .models import Shipping
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

def shippingList(request):
    all_shippings = Shipping.objects.all().order_by("-id") #

    return render(request, 'naver/shippingList.html', {'title':'Shipping List', 'shipping_list':all_shippings})

def shippingAdd(request):
    return render(request, 'naver/shippingAdd.html')

def shippingUpdate(request, shipping_id):
    shipping = Shipping.objects.get(pk=shipping_id)
    return render(request, 'naver/shippingAdd.html', {'shipping': shipping})

def shippingSave(request, shipping_id):
    print("===" * 10)
    
    print(request.POST)
    shipping = {}
    if shipping_id != 0:
        shipping = Shipping.objects.get(pk=shipping_id)
    else:
        shipping = Shipping()
    shipping.title = request.POST['title']
    shipping.cost_template_code = request.POST['cost_template_code']
    shipping.type = request.POST['type']
    shipping.courier_code = request.POST['courier_code']
    shipping.default_cost = request.POST['default_cost']
    shipping.cost_type = request.POST['cost_type']
    shipping.save()
    return HttpResponseRedirect(reverse('shippingList'))

def shippingDetail(request, shipping_id):
    shipping = Shipping.objects.get(id=shipping_id)
    return render(request, 'naver/shippingDetail.html', {'shipping': shipping})

def shippingDel(request, shipping_id):
    try:
        shipping = Shipping.objects.get(pk=shipping_id)
        shipping.delete()
    except:
        pass
    return HttpResponseRedirect(reverse('shippingList'))

