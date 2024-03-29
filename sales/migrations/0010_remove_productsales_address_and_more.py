# Generated by Django 4.2.3 on 2023-07-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0009_rename_products_productsales_product_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productsales",
            name="address",
        ),
        migrations.RemoveField(
            model_name="productsales",
            name="business_name",
        ),
        migrations.RemoveField(
            model_name="productsales",
            name="business_pin",
        ),
        migrations.RemoveField(
            model_name="productsales",
            name="receipt_label",
        ),
        migrations.AddField(
            model_name="sales",
            name="address",
            field=models.CharField(default="21 Jump Street", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="sales",
            name="business_name",
            field=models.CharField(default="General Stores", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="sales",
            name="business_pin",
            field=models.CharField(default="A345678WERTY", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="sales",
            name="receipt_label",
            field=models.CharField(default="NS", max_length=5),
            preserve_default=False,
        ),
    ]
