# Generated by Django 3.1.1 on 2021-04-05 22:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_auto_20210405_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 22, 55, 10, 602375, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='seeker',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 22, 55, 10, 608144, tzinfo=utc)),
        ),
    ]