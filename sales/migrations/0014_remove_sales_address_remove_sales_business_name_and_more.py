# Generated by Django 4.2.3 on 2023-07-15 10:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0013_rename_product_id_productsales_product_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sales",
            name="address",
        ),
        migrations.RemoveField(
            model_name="sales",
            name="business_name",
        ),
        migrations.RemoveField(
            model_name="sales",
            name="business_pin",
        ),
    ]
