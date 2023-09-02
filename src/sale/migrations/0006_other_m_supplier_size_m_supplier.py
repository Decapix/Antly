# Generated by Django 4.1.7 on 2023-08-23 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_supplier', '0001_initial'),
        ('sale', '0005_order_m_shipping_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='other_m',
            name='supplier',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='other', to='admin_supplier.supplier_m'),
        ),
        migrations.AddField(
            model_name='size_m',
            name='supplier',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='admin_supplier.supplier_m'),
        ),
    ]