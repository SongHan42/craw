from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crawling', views.crawling, name="crawling"),
    path('excel', views.excel, name="excel"),
    path('shippingList', views.shippingList, name="shippingList"),
    path('shippingAdd/<int:shipping_id>', views.shippingUpdate, name="shippingUpdate"),
    path('shippingAdd', views.shippingAdd, name="shippingAdd"),
    path('shippingAdd/save/<int:shipping_id>', views.shippingSave, name='shippingSave'),
    path('shipping/<int:shipping_id>', views.shippingDetail, name='shippingDetail'),
    path('shipping/del/<int:shipping_id>', views.shippingDel, name='shippingDel'),
    path('fileupload', views.fileUpload, name="fileupload")
]