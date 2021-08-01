# Generated by Django 3.1.1 on 2021-04-05 12:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20210405_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 22, 5, 10, 352939)),
        ),
        migrations.AlterField(
            model_name='employer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='seeker',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 22, 5, 10, 358688)),
        ),
        migrations.AlterField(
            model_name='seeker',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
