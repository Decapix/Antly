# Generated by Django 4.1.7 on 2023-03-24 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_address_m_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopper_m',
            name='address',
        ),
        migrations.AddField(
            model_name='address_m',
            name='shopper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
