# Generated by Django 4.2.3 on 2023-07-19 16:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0005_alter_product_tax_type"),
        ("administration", "0006_delete_customer"),
        ("sales", "0014_remove_sales_address_remove_sales_business_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Purchase",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("product_quantity", models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ("purchase_amount", models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "product_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchases",
                        to="products.stock",
                    ),
                ),
                (
                    "supplier_id",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchases",
                        to="administration.supplier",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchases",
                        to="administration.employee",
                    ),
                ),
            ],
        ),
    ]