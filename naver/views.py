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
    main.crawling(request.POST['url'])
    return HttpResponseRedirect(reverse('index'))

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

class ProductListView(generic.ListView):
    template_name = 'naver/product_page.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.all()

def detailView(request, id):
    if request.method == "GET":
        product = Product.objects.get(pk=id)
        template = loader.get_template('naver/detail.html')
        context = {
            'product': product
        }
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        print(request.POST)
        product = Product.objects.get(pk=id)
        product.product_name = request.POST["name"]
        product.product_state = request.POST["state"]
        product.product_price = request.POST["price"]
        product.vat = request.POST["vat"]
        product.stock_num = request.POST["stock_num"]
        product.option_type = request.POST["option_type"]
        product.pc_instant_discount_value = request.POST["pc_instant_discount_value"]
        if request.POST.get("pc_instant_discount_unit"):
            product.pc_instant_discount_unit = request.POST["pc_instant_discount_unit"]
        product.mobile_instant_discount_value = request.POST["mobile_instant_discount_value"]
        if request.POST.get("mobile_instant_discount_unit"):
            product.mobile_instant_discount_unit = request.POST["mobile_instant_discount_unit"]
        product.multiple_purchase_discount_condition_value = request.POST["multiple_purchase_discount_condition_value"]
        if request.POST.get("multiple_purchase_discount_condition_unit"):
            product.multiple_purchase_discount_condition_unit = request.POST["multiple_purchase_discount_condition_unit"]
        product.multiple_purchase_discount_value = request.POST["multiple_purchase_discount_value"]
        if request.POST.get("multiple_purchase_discount_unit"):
            product.multiple_purchase_discount_unit = request.POST["multiple_purchase_discount_unit"]
        product.interset_free_installment_month = request.POST["interset_free_installment_month"]
        product.gift = request.POST["gift"]
        if request.POST["review_exposure_state"] == "True":
            product.review_exposure_state = True
        else:
            product.review_exposure_state = False
        product.review_non_exposure_reson = request.POST["review_non_exposure_reson"]
        after_service = product.afterservice_set.get()
        after_service.phone_number = request.POST["after_service_phone_number"]
        after_service.announcement = request.POST["after_service_announcement"]
        after_service.seller_specifics = request.POST["after_service_seller_specifics"]
        product.save()
        after_service.save()
        return HttpResponseRedirect(reverse('product'))

def update(request, id):
    return HttpResponseRedirect(reverse('product'))
