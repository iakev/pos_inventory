# Generated by Django 4.2.3 on 2023-07-10 14:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_alter_stock_options_remove_category_slug_and_more"),
        ("sales", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sales",
            options={"ordering": ["time_created"], "verbose_name_plural": "sales"},
        ),
        migrations.RemoveField(
            model_name="sales",
            name="time_paid",
        ),
        migrations.AddField(
            model_name="paymentmode",
            name="uuid",
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name="sales",
            name="uuid",
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.CreateModel(
            name="ProductSales",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("quantity_sold", models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ("price_per_unit", models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ("is_wholesale", models.BooleanField(default=False)),
                ("price", models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ("tax_amount", models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ("receipt_label", models.CharField(max_length=5)),
                ("tax_rate", models.CharField(max_length=5)),
                ("business_name", models.CharField(max_length=255)),
                ("business_pin", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                (
                    "products",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="products", to="products.product"
                    ),
                ),
                (
                    "sales",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="sales", to="sales.sales"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="sales",
            name="products",
            field=models.ManyToManyField(related_name="sales", through="sales.ProductSales", to="products.product"),
        ),
    ]
