# Generated by Django 3.1.1 on 2021-03-17 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employerapp', '0006_auto_20210317_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='failed',
            field=models.BooleanField(default=False, verbose_name='вакансия не прошла модерацию'),
        ),
    ]
