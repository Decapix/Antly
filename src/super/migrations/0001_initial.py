# Generated by Django 4.1.7 on 2023-03-30 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offer_m',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('message', models.CharField(max_length=100)),
                ('text', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
