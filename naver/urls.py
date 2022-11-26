from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crawling', views.crawling, name="crawling"),
    path('excel', views.excel, name="excel"),
    path('fileupload', views.fileUpload, name="fileupload"),
    path('product', views.ProductListView.as_view(), name="product"),
    path('product/<int:id>', views.detailView, name="product_detail"),
]