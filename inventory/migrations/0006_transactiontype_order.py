# Generated by Django 5.0 on 2024-01-03 16:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0005_transactiontype_alter_product_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="transactiontype",
            name="order",
            field=models.IntegerField(default=-1),
        ),
    ]
