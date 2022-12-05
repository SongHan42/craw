from sre_constants import MAX_UNTIL
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Shipping(models.Model):
    # Type = (
    #     ("택배, 소포, 등기", "delivery"),
    #     ("직접배송(화물배달)", "direct_delivery")
    # )

    # CostType = (
    #     ("무료", "free"),
    #     ("조건부 무료", "conditionally_free"),
    #     ("유료", "charged"),
    #     ("수량별", "by_quantity"),
    #     ("구간별", "by_section")
    # )

    # CostPaymentType = (
    #     ("착불", "pay_on_delivery"),
    #     ("선결제", "prepayment"),
    #     ("착불 또는 선결제", "all")
    # )
    title = models.CharField(max_length = 200, default="")
    cost_template_code = models.IntegerField(null = True)
    # type = models.CharField(max_length = 30, null = True, choices = Type)
    type = models.CharField(max_length = 30, default="")
    courier_code = models.CharField(max_length = 30, null = True)
    # cost_type = models.CharField(max_length = 10, null = True, choices = CostType)
    cost_type = models.CharField(max_length = 10, default="무료")
    default_cost = models.IntegerField(null = True)
    cost_payment_type = models.CharField(max_length = 10, default="선결제")
    # cost_payment_type = models.CharField(max_length = 10, null = True, choices = CostPaymentType)
    
    # "조건부무료-
    # 상품판매가 합계"	수량별부과-수량	"구간별-
    # 2구간수량"	"구간별-
    # 3구간수량"	"구간별-
    # 3구간배송비"	"구간별-
    # 추가배송비"
    return_cost = models.IntegerField(null = True)
    exchange_cost = models.IntegerField(null = True)
    # 지역별 차등 배송비
    extra_installation_cost = models.IntegerField(null = True)


class Product(models.Model):
    # ProductState = (
    #     ("신상품", "new"),
    #     ("중고상품", "used")
    # )

    # Vat = (
    #     ("과세", "taxation"),
    #     ("면세", "duty_free"),
    #     ("비과세", "tax_free")
    # )

    # Unit = (
    #     ("%", "percent"),
    #     ("원", "won")
    # )

    # MultpleDiscountUnit = (
    #     ("개", "num"),
    #     ("원", "won")
    # )

    category_code = models.IntegerField()
    product_name = models.CharField(max_length = 200)
    # product_state = models.CharField(max_length = 10, choices = ProductState)
    product_state = models.CharField(max_length = 10)
    product_price = models.IntegerField()
    # vat = models.CharField(max_length = 10, choices = Vat)
    vat = models.CharField(max_length = 10, default="과세상품")
    stock_num = models.IntegerField()
    option_type = models.CharField(max_length = 10, default="")
    main_img = models.CharField(max_length = 255)
    # 상세설명 = ""
    detail_descript = RichTextUploadingField(blank=True,null=True)
    brand = models.CharField(max_length = 50, default="")
    manufacturer = models.CharField(max_length = 50, default="")
    manufacturing_date = models.DateField(null = True)
    effective_date = models.DateField(null = True)
    origin_code = models.CharField(max_length=10)
    importer = models.CharField(max_length = 50)
    is_plural_origin = models.BooleanField(default=False)
    origin_direct_input = models.CharField(max_length = 50, default="")
    # is_minor = models.BooleanField()
    shipping = models.ForeignKey(Shipping, on_delete = models.SET_NULL, null = True)
    info_template_code = models.IntegerField(null = True)
    info_name = models.CharField(max_length = 100, default="")
    info_model_name = models.CharField(max_length = 100, default="")
    info_authorization = models.TextField(default="")
    info_manufacturer = models.TextField(default="")
    # after_service = models.ForeignKey(AfterService, on_delete = models.SET_NULL, null = True)
    pc_instant_discount_value = models.IntegerField(default=0)
    # pc_instant_discount_unit = models.CharField(max_length = 10, null = True, choices = Unit)
    pc_instant_discount_unit = models.CharField(max_length = 10, default="")
    mobile_instant_discount_value = models.IntegerField(default=0)
    # mobile_instant_discount_unit = models.CharField(max_length = 10, null = True, choices = Unit)
    mobile_instant_discount_unit = models.CharField(max_length = 10, default="")
    multiple_purchase_discount_condition_value = models.IntegerField(default=0)
    # multiple_purchase_discount_condition_unit = models.CharField(max_length = 10, null = True, choices = MultpleDiscountUnit)
    multiple_purchase_discount_condition_unit = models.CharField(max_length = 10, default="")
    multiple_purchase_discount_value = models.IntegerField(default=0)
    # multiple_purchase_discount_unit = models.CharField(max_length = 10, null = True, choices = Unit)
    multiple_purchase_discount_unit = models.CharField(max_length = 10, default="")
    # 포인트

    interset_free_installment_month = models.IntegerField(default=0)
    gift = models.CharField(max_length = 100, default="")
    # 판매자 바코드
    review_exposure_state = models.BooleanField(default=True)
    review_non_exposure_reson = models.TextField(default="")
    # "스토어찜회원 전용여부"

class AfterService(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    template_code = models.IntegerField(null = True)
    phone_number = models.CharField(max_length = 20, default="")
    announcement = models.TextField(default="")
    seller_specifics = models.TextField(default="")


class Book(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    ISBN = models.IntegerField(null = True)
    ISSN = models.IntegerField(null = True)
    is_independent_publication = models.BooleanField(default=False)
    publication_date = models.DateField(null = True)
    publisher = models.CharField(max_length = 100, default="")
    writer = models.CharField(max_length = 100, default="")
    painter = models.CharField(max_length = 100, default="")
    translator = models.CharField(max_length = 100, default="")
    is_cultural_expenses_income_tax_deduction = models.BooleanField(default=True)

# class OptionType(models.Model):
#     # OptionType = (
#     #     ("단독", "solitary"),
#     #     ("조합", "combination")
#     # )

#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     # option_type = models.CharField(max_length = 10, choices=OptionType)
#     option_type = models.CharField(max_length = 10)

class OptionName(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Option(models.Model):
    option_name = models.ForeignKey(OptionName, on_delete = models.CASCADE)
    value = models.CharField(max_length = 50)
    price = models.IntegerField()

class OptionStockNum(models.Model):
    option = models.ForeignKey(Option, on_delete = models.CASCADE)
    num = models.IntegerField()

class DirectInputOption(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    text = models.CharField(max_length = 50)

class AdditionalProductName(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)

class AdditionalProductDetail(models.Model):
    additional_product_name = models.ForeignKey(AdditionalProductName, on_delete=models.CASCADE)
    value = models.CharField(max_length = 50)
    price = models.IntegerField()
    num = models.IntegerField()

class SubImg(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    img = models.CharField(max_length = 255)