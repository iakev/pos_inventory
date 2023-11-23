# Generated by Django 4.2.3 on 2023-09-25 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("administration", "0007_remove_business_owner_owner"),
        ("sales", "0015_purchase"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sales",
            name="business_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sale",
                to="administration.business",
            ),
        ),
    ]
