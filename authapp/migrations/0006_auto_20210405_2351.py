# Generated by Django 3.1.1 on 2021-04-05 13:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_auto_20210405_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 23, 51, 41, 726689)),
        ),
        migrations.AlterField(
            model_name='seeker',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 23, 51, 41, 731869)),
        ),
    ]
