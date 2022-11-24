from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crawling', views.crawling, name="crawling"),
    path('excel', views.excel, name="excel"),
    path('shipping/add')
    path('fileupload', views.fileUpload, name="fileupload")
]