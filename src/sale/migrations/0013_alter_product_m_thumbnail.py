# Generated by Django 4.1.7 on 2024-02-15 15:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sale", "0012_remove_order_m_shipping_type_order_m_delivery_option"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product_m",
            name="thumbnail",
            field=models.ImageField(upload_to="products"),
        ),
    ]
