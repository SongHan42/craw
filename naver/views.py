from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.template import loader
from .models import *

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