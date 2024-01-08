# Generated by Django 4.2.3 on 2023-11-21 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("administration", "0012_alter_owner_business"),
        ("sales", "0031_purchaseproduct_supplier"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sales",
            name="employee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sales",
                to="administration.employee",
            ),
        ),
    ]