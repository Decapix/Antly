# Generated by Django 4.1.7 on 2023-05-10 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0009_nest_m_alter_pack_m_size_alter_size_m_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_m',
            name='order_track',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
