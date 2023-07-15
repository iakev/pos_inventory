# Generated by Django 4.2.3 on 2023-07-13 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0005_delete_transactiontype_alter_paymentmode_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sales",
            options={"ordering": ["created_at", "updated_at"], "verbose_name_plural": "sales"},
        ),
        migrations.RemoveField(
            model_name="sales",
            name="time_created",
        ),
        migrations.AlterField(
            model_name="sales",
            name="payment_id",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sale",
                to="sales.paymentmode",
            ),
        ),
    ]
