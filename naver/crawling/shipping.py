from ..models import Shipping
from django.core.paginator import Paginator

def shipping_list(page):
    all_shippings = Shipping.objects.all().order_by("-pub_date") #내림차순
    paginator = Paginator(all_shippings, 5)
    board_list = paginator.get_page(page)
# def shipping_add()