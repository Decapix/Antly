# Generated by Django 4.1.7 on 2023-08-26 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_shopper_m_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopper_m',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
