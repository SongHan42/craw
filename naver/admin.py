from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

# Register your models here.

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "cost_type",
        "default_cost"
    )

# class OptionInline(admin.TabularInline):
#     model = Option

# class OptionNameInline(admin.TabularInline):
#     model = OptionName

#     fields = ["name"]
#     show_change_link = True
    
class OptionInline(NestedStackedInline):
    model = Option
    extra = 1

class OptionNameInline(NestedStackedInline):
    model = OptionName
    inlines = [OptionInline]
    extra = 1

@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    inlines = [OptionNameInline]

class SubImgInline(admin.TabularInline):
    model = SubImg

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [SubImgInline]

#     list_display = ["name"]

    # fields = ["SubImg.render_image"]

# admin.site.register(Shipping)
admin.site.register(AfterService)
# admin.site.register(Product)
admin.site.register(Book)
# admin.site.register(OptionName)
# admin.site.register(Option)
admin.site.register(OptionStockNum)
admin.site.register(DirectInputOption)
admin.site.register(AdditionalProductName)
admin.site.register(AdditionalProductDetail)
admin.site.register(SubImg)