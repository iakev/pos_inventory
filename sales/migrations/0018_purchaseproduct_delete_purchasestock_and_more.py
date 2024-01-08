# Generated by Django 4.2.3 on 2023-11-02 17:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_supplierproduct_lead_time"),
        ("sales", "0017_remove_purchase_product_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PurchaseProduct",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("product_quantity", models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ("purchase_unit_price", models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ("total_product_cost", models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("discount_applied", models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchase_products",
                        to="products.product",
                    ),
                ),
                (
                    "purchase",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchase_products",
                        to="sales.purchase",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="PurchaseStock",
        ),
        migrations.AlterField(
            model_name="purchase",
            name="products",
            field=models.ManyToManyField(
                related_name="purchases", through="sales.PurchaseProduct", to="products.product"
            ),
        ),
    ]