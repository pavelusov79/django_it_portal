# Generated by Django 3.1.1 on 2021-03-10 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employerapp', '0002_auto_20210310_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='currency',
            field=models.CharField(blank=True, choices=[('rub', 'руб.'), ('usd', 'USD')], help_text='поле необязательное для заполнения', max_length=4, verbose_name='валюта'),
        ),
    ]
