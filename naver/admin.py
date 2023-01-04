from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

class OptionStockNumInline(NestedStackedInline):
    model = OptionStockNum
    extra = 1

class OptionInline(NestedStackedInline):
    model = Option
    inlines = [OptionStockNumInline]
    extra = 1

class OptionNameInline(NestedStackedInline):
    model = OptionName
    inlines = [OptionInline]
    extra = 1

class DirectInputOptionInline(admin.StackedInline):
    model = DirectInputOption
    extra = 0

class AdditionalProductDetailInline(NestedStackedInline):
    model = AdditionalProductDetail
    extra = 1

class AdditionalProductNameInline(NestedStackedInline):
    model = AdditionalProductName
    inlines = [AdditionalProductDetailInline]
    extra = 1

class SubImgInline(admin.StackedInline):
    model = SubImg
    extra = 1

class BookInline(admin.StackedInline):
    model = Book
    extra = 0

@admin.action(description="배송 기본 설정(첫 택배 템플릿 골라짐)")
def default_shipping(modeladmin, request, queryset):
    shipping = Shipping.objects.all()
    if not shipping:
        shipping = Shipping()
        shipping.title = "기본 배송"
        shipping.type = "택배, 소포, 등기"
        shipping.cost_type = "무료"
        shipping.cost_payment_type = "선결제"
        shipping.save()
    else:
        shipping = shipping[0]
    queryset.update(shipping=shipping)

@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    inlines = [
        OptionNameInline,
        DirectInputOptionInline,
        AdditionalProductNameInline,
        SubImgInline,
        BookInline
    ]

    search_fields = ['name']

    list_display = (
        'id',
        'name',
    )

    actions = [default_shipping]

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "cost_type",
        "default_cost"
    )

@admin.register(AfterService)
class AfterServiceAdmin(admin.ModelAdmin):
    pass

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(OptionStockNum)
# admin.site.register(DirectInputOption)
# admin.site.register(AdditionalProductName)
# admin.site.register(AdditionalProductDetail)
# admin.site.register(SubImg)