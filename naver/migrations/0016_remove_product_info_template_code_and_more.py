# Generated by Django 4.1.2 on 2022-12-05 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('naver', '0015_alter_afterservice_announcement_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='info_template_code',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_state',
        ),
        migrations.RemoveField(
            model_name='shipping',
            name='cost_template_code',
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default='', max_length=200, verbose_name='상품명'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0, verbose_name='판매가'),
        ),
        migrations.AddField(
            model_name='product',
            name='state',
            field=models.CharField(choices=[('신상품', '신상품'), ('중고상품', '중고상품')], default='신상품', max_length=10, verbose_name='상품상태'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='브랜드'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category_code',
            field=models.IntegerField(verbose_name='카테고리 코드'),
        ),
        migrations.AlterField(
            model_name='product',
            name='effective_date',
            field=models.DateField(blank=True, null=True, verbose_name='유효일자'),
        ),
        migrations.AlterField(
            model_name='product',
            name='gift',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='사은품'),
        ),
        migrations.AlterField(
            model_name='product',
            name='importer',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='수입사'),
        ),
        migrations.AlterField(
            model_name='product',
            name='info_authorization',
            field=models.TextField(blank=True, default='', verbose_name='상품정보제공고시 인증허가사항'),
        ),
        migrations.AlterField(
            model_name='product',
            name='info_manufacturer',
            field=models.TextField(blank=True, default='', verbose_name='상품정보제공고시 제조자'),
        ),
        migrations.AlterField(
            model_name='product',
            name='info_model_name',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='상품정보제공고시 모델명'),
        ),
        migrations.AlterField(
            model_name='product',
            name='info_name',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='상품정보제공고시 품명'),
        ),
        migrations.AlterField(
            model_name='product',
            name='interset_free_installment_month',
            field=models.IntegerField(default=0, verbose_name='무이자 할부 개월'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_plural_origin',
            field=models.BooleanField(default=False, verbose_name='복수원산지여부'),
        ),
        migrations.AlterField(
            model_name='product',
            name='main_img',
            field=models.ImageField(upload_to='', verbose_name='대표이미지'),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturer',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='제조사'),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturing_date',
            field=models.DateField(blank=True, null=True, verbose_name='제조일자'),
        ),
        migrations.AlterField(
            model_name='product',
            name='mobile_instant_discount_unit',
            field=models.CharField(choices=[('', ''), ('%', '%'), ('원', '원')], default='원', max_length=10, verbose_name='모바일 즉시할인 단위'),
        ),
        migrations.AlterField(
            model_name='product',
            name='mobile_instant_discount_value',
            field=models.IntegerField(default=0, verbose_name='모바일 즉시할인 값'),
        ),
        migrations.AlterField(
            model_name='product',
            name='multiple_purchase_discount_condition_unit',
            field=models.CharField(choices=[('개', '개'), ('원', '원')], default='개', max_length=10, verbose_name='복수구매할인 조건 단위'),
        ),
        migrations.AlterField(
            model_name='product',
            name='multiple_purchase_discount_condition_value',
            field=models.IntegerField(default=0, verbose_name='복수구매할인 조건 값'),
        ),
        migrations.AlterField(
            model_name='product',
            name='multiple_purchase_discount_unit',
            field=models.CharField(choices=[('', ''), ('%', '%'), ('원', '원')], default='원', max_length=10, verbose_name='복수구매할인 단위'),
        ),
        migrations.AlterField(
            model_name='product',
            name='multiple_purchase_discount_value',
            field=models.IntegerField(default=0, verbose_name='복수구매할인 값'),
        ),
        migrations.AlterField(
            model_name='product',
            name='option_type',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='옵션형태'),
        ),
        migrations.AlterField(
            model_name='product',
            name='origin_code',
            field=models.CharField(max_length=10, verbose_name='원산지'),
        ),
        migrations.AlterField(
            model_name='product',
            name='origin_direct_input',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='원산지 직접입력'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pc_instant_discount_unit',
            field=models.CharField(choices=[('', ''), ('%', '%'), ('원', '원')], default='원', max_length=10, verbose_name='PC 즉시할인 단위'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pc_instant_discount_value',
            field=models.IntegerField(default=0, verbose_name='PC 즉시할인 값'),
        ),
        migrations.AlterField(
            model_name='product',
            name='review_exposure_state',
            field=models.BooleanField(default=True, verbose_name='구매평 노출여부'),
        ),
        migrations.AlterField(
            model_name='product',
            name='review_non_exposure_reson',
            field=models.TextField(default='', verbose_name='구매평 비노출사유'),
        ),
        migrations.AlterField(
            model_name='product',
            name='shipping',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='naver.shipping', verbose_name='택배'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock_num',
            field=models.IntegerField(verbose_name='재고수량'),
        ),
        migrations.AlterField(
            model_name='product',
            name='vat',
            field=models.CharField(choices=[('과세상품', '과세상품'), ('면세상품', '면세상품'), ('영세상품', '영세상품')], default='과세상품', max_length=10, verbose_name='부가세'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='cost_payment_type',
            field=models.CharField(blank=True, choices=[('', ''), ('착불', '착불'), ('선결제', '선결제'), ('착불 또는 선결제', '착불 또는 선결제')], max_length=10, verbose_name='배송비 결재방식'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='cost_type',
            field=models.CharField(blank=True, choices=[('', ''), ('무료', '무료'), ('조건부 무료', '조건부 무료'), ('유료', '유료'), ('수량별', '수량별'), ('구간별', '구간별')], max_length=10, verbose_name='배송비유형'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='courier_code',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='택배사코드'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='default_cost',
            field=models.IntegerField(blank=True, null=True, verbose_name='기본배송비'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='exchange_cost',
            field=models.IntegerField(blank=True, null=True, verbose_name='교환배송비'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='extra_installation_cost',
            field=models.IntegerField(blank=True, null=True, verbose_name='별도설치비'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='return_cost',
            field=models.IntegerField(blank=True, null=True, verbose_name='반품배송비'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='title',
            field=models.CharField(default='', max_length=200, verbose_name='제목'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='type',
            field=models.CharField(blank=True, choices=[('', ''), ('택배, 소포, 등기', '택배, 소포, 등기'), ('직접배송(화물배달)', '직접배송(화물배달)')], max_length=30, verbose_name='배송방법'),
        ),
    ]
