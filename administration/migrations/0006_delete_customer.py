# Generated by Django 4.2.3 on 2023-07-13 09:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0004_customer_alter_paymentmode_properties_and_more"),
        ("administration", "0005_employee_email_address"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Customer",
        ),
    ]