# Generated by Django 3.1.1 on 2021-04-05 13:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20210405_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 23, 38, 41, 745623)),
        ),
        migrations.AlterField(
            model_name='seeker',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 13, 38, 41, 859943, tzinfo=utc)),
        ),
    ]