# Generated by Django 4.1.2 on 2022-11-25 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naver', '0013_rename_name_shipping_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='courier_code',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
