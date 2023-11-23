# Generated by Django 4.2.3 on 2023-09-28 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("administration", "0011_rename_owner_owner_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="owner",
            name="business",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owners",
                to="administration.business",
            ),
        ),
    ]
