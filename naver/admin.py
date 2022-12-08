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

@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    inlines = [
        OptionNameInline,
        DirectInputOptionInline,
        AdditionalProductNameInline,
        SubImgInline,
        BookInline
    ]

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