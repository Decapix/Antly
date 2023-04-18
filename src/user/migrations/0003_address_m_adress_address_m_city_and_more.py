# Generated by Django 4.1.7 on 2023-03-24 14:37

from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_shopper_m_address_delete_address_m'),
    ]

    operations = [
        migrations.AddField(
            model_name='address_m',
            name='adress',
            field=models.CharField(default='address', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address_m',
            name='city',
            field=models.CharField(default='city', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address_m',
            name='complete_name',
            field=models.CharField(default='name', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address_m',
            name='country',
            field=models.CharField(default='country', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address_m',
            name='detail',
            field=models.CharField(default='detail', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address_m',
            name='phone_number',
            field=models.CharField(default='0651336159', max_length=30, validators=[user.models.validate_phone_number]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address_m',
            name='postal_code',
            field=models.CharField(default='77000', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopper_m',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.address_m'),
        ),
    ]
