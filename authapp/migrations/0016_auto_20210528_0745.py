# Generated by Django 3.2.3 on 2021-05-28 07:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0015_auto_20210528_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 29, 7, 45, 26, 85495)),
        ),
        migrations.AlterField(
            model_name='seeker',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 29, 7, 45, 26, 92321)),
        ),
    ]
