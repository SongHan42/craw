from sre_constants import MAX_UNTIL
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from .common import image_upload_path

# Create your models here.

class Shipping(models.Model):
    class TypeChoices(models.TextChoices):
        BRANK = "", ""
        DELIVERY = "택배, 소포, 등기", "택배, 소포, 등기"
        DIRECT_DELIVERY = "직접배송(화물배달)", "직접배송(화물배달)"

    class CostTypeChoices(models.TextChoices):
        BRANK = "", ""
        FREE = "무료", "무료"
        CONDITIONALLY_FREE = "조건부 무료", "조건부 무료"
        CHARGED = "유료", "유료"
        BY_QUANTITY = "수량별", "수량별"
        BY_SECTION = "구간별", "구간별"

    class CostPaymentTypeChoices(models.TextChoices):
        BRANK = "", ""
        PAY_ON_DELIVERY = "착불", "착불"
        PREPAYMENT = "선결제", "선결제"
        ALL = "착불 또는 선결제", "착불 또는 선결제"
    
    title = models.CharField(max_length = 200, verbose_name="제목")
    # cost_template_code = models.IntegerField(null = True)
    type = models.CharField(max_length = 30, choices=TypeChoices.choices, blank=True, verbose_name="배송방법")
    courier_code = models.CharField(max_length = 30, default="", blank=True, verbose_name="택배사코드")
    cost_type = models.CharField(max_length = 10, choices=CostTypeChoices.choices, blank=True, verbose_name="배송비유형")
    default_cost = models.IntegerField(null = True, blank=True, verbose_name="기본배송비")
    cost_payment_type = models.CharField(max_length = 10, choices=CostPaymentTypeChoices.choices, blank=True, verbose_name="배송비 결재방식")
    
    # "조건부무료-
    # 상품판매가 합계"	수량별부과-수량	"구간별-
    # 2구간수량"	"구간별-
    # 3구간수량"	"구간별-
    # 3구간배송비"	"구간별-
    # 추가배송비"
    return_cost = models.IntegerField(null = True, blank=True, verbose_name="반품배송비")
    exchange_cost = models.IntegerField(null = True, blank=True, verbose_name="교환배송비")
    # 지역별 차등 배송비
    extra_installation_cost = models.IntegerField(null = True, blank=True, verbose_name="별도설치비")

    def __str__(self):
        return self.title


class Product(models.Model):
    class StateChoices(models.TextChoices):
        NEW = "신상품", "신상품"
        USED = "중고상품", "중고상품"

    class VatChoices(models.TextChoices):
        TAXATION = "과세상품", "과세상품"
        DUTY_FREE = "면세상품", "면세상품"
        TAX_FREE = "영세상품", "영세상품"

    class UnitChoices(models.TextChoices):
        BLANK = "", ""
        PERCENT = "%", "%"
        WON = "원", "원"

    class MultpleDiscountUnitChoices(models.TextChoices):
        NUM = "개", "개"
        WON = "원", "원"

    class OptionTypeChoices(models.TextChoices):
        BLANK = "", ""
        SOLITARY = "단독형", "단독형"
        COMBINATION = "조합형", "조합형"

    name = models.CharField(max_length = 200, verbose_name="상품명")
    #???????????
    category_code = models.IntegerField(verbose_name="카테고리 코드")
    state = models.CharField(max_length = 10, default="신상품", choices=StateChoices.choices, verbose_name="상품상태")
    price = models.IntegerField(verbose_name="판매가")
    vat = models.CharField(max_length = 10, default="과세상품", choices=VatChoices.choices, verbose_name="부가세")
    stock_num = models.IntegerField(verbose_name="재고수량")
    option_type = models.CharField(max_length = 10, default="", choices=OptionTypeChoices.choices, blank=True, verbose_name="옵션형태")
    # 이미지
    main_img = models.ImageField(max_length=300, verbose_name="대표이미지", upload_to=image_upload_path)
    detail_description = RichTextUploadingField(blank=True,null=True)
    brand = models.CharField(max_length = 50, default="", verbose_name="브랜드")
    manufacturer = models.CharField(max_length = 50, default="", blank=True, verbose_name="제조사")
    manufacturing_date = models.DateField(null = True, blank=True, verbose_name="제조일자")
    effective_date = models.DateField(null = True, blank=True, verbose_name="유효일자")
    origin_code = models.CharField(max_length=10, verbose_name="원산지코드")
    importer = models.CharField(max_length = 50, blank=True, verbose_name="수입사")
    is_plural_origin = models.BooleanField(default=False, verbose_name="복수원산지여부")
    origin_direct_input = models.CharField(max_length = 50, default="", blank=True, verbose_name="원산지 직접입력")
    # is_minor = models.BooleanField()
    shipping = models.ForeignKey(Shipping, on_delete = models.SET_NULL, null = True, blank=True, verbose_name="택배")
    # info_template_code = models.IntegerField(null = True)
    info_name = models.CharField(max_length = 100, default="", blank=True, verbose_name="상품정보제공고시 품명")
    info_model_name = models.CharField(max_length = 100, default="", blank=True, verbose_name="상품정보제공고시 모델명")
    info_authorization = models.TextField(default="", blank=True, verbose_name="상품정보제공고시 인증허가사항")
    info_manufacturer = models.TextField(default="", blank=True, verbose_name="상품정보제공고시 제조자")
    # after_service = models.ForeignKey(AfterService, on_delete = models.SET_NULL, null = True)
    pc_instant_discount_value = models.IntegerField(default=0, verbose_name="PC 즉시할인 값")
    pc_instant_discount_unit = models.CharField(max_length = 10, default="원", choices=UnitChoices.choices, verbose_name="PC 즉시할인 단위")
    mobile_instant_discount_value = models.IntegerField(default=0, verbose_name="모바일 즉시할인 값")
    mobile_instant_discount_unit = models.CharField(max_length = 10, default="원", choices = UnitChoices.choices, verbose_name="모바일 즉시할인 단위")
    multiple_purchase_discount_condition_value = models.IntegerField(default=0, verbose_name="복수구매할인 조건 값")
    multiple_purchase_discount_condition_unit = models.CharField(max_length = 10, default="개", choices = MultpleDiscountUnitChoices.choices, verbose_name="복수구매할인 조건 단위")
    multiple_purchase_discount_value = models.IntegerField(default=0, verbose_name="복수구매할인 값")
    multiple_purchase_discount_unit = models.CharField(max_length = 10, default="원", choices = UnitChoices.choices, verbose_name="복수구매할인 단위")
    # 포인트

    interset_free_installment_month = models.IntegerField(default=0, verbose_name="무이자 할부 개월")
    gift = models.CharField(max_length = 100, default="", blank=True, verbose_name="사은품")
    # 판매자 바코드
    review_exposure_state = models.BooleanField(default=True, verbose_name="구매평 노출여부")
    review_non_exposure_reson = models.TextField(default="", blank=True, verbose_name="구매평 비노출사유")
    # "스토어찜회원 전용여부"

    url = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return self.name

class AfterService(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="상품명")
    template_code = models.IntegerField(null = True)
    phone_number = models.CharField(max_length = 20, verbose_name="A/S 전화번호")
    announcement = models.TextField(verbose_name="A/S 안내사항")
    seller_specifics = models.TextField(default="", verbose_name="판매자특이사항")

    def __str__(self):
        return self.product.name

class Book(models.Model):
    # product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name="상품명")
    product = models.OneToOneField(Product, on_delete = models.CASCADE, verbose_name="상품명")
    ISBN = models.IntegerField(default=0, blank=True)
    ISSN = models.IntegerField(default=0, blank=True)
    is_independent_publication = models.BooleanField(default=False, blank=True, verbose_name="독립출판")
    publication_date = models.DateField(null = True, blank=True, verbose_name="출간일")
    publisher = models.CharField(max_length = 100, default="", blank=True, verbose_name="출판사")
    writer = models.CharField(max_length = 100, default="", blank=True, verbose_name="글작가")
    painter = models.CharField(max_length = 100, default="", blank=True, verbose_name="그림작가")
    translator = models.CharField(max_length = 100, default="", blank=True, verbose_name="번역자명")
    is_cultural_expenses_income_tax_deduction = models.BooleanField(default=False, verbose_name="문화비 소득공제")

class OptionName(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="상품")
    name = models.CharField(max_length=50, verbose_name="옵션명")

class Option(models.Model):
    option_name = models.ForeignKey(OptionName, on_delete = models.CASCADE, verbose_name="옵션")
    value = models.CharField(max_length = 50, verbose_name="옵션값")
    price = models.IntegerField(verbose_name="옵션가")

class OptionStockNum(models.Model):
    option = models.OneToOneField(Option, on_delete=models.CASCADE, verbose_name="옵션")
    num = models.IntegerField(verbose_name="재고수량")

class DirectInputOption(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name="상품")
    text = models.CharField(max_length = 50, verbose_name="옵션명")

class AdditionalProductName(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="상품")
    name = models.CharField(max_length = 50, verbose_name="추가상품명")

class AdditionalProductDetail(models.Model):
    additional_product_name = models.ForeignKey(AdditionalProductName, on_delete=models.CASCADE, verbose_name="추가상품명")
    value = models.CharField(max_length = 50, verbose_name="추가상품값")
    price = models.IntegerField(verbose_name="상품가")
    num = models.IntegerField(verbose_name="재고수량")

class SubImg(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    img = models.ImageField(max_length=300, upload_to=image_upload_path)
