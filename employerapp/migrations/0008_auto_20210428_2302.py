# Generated by Django 3.1.1 on 2021-04-28 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employerapp', '0007_vacancy_failed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='action',
            field=models.CharField(choices=[('draft', 'сохранить черновик'), ('publish', 'опубликовать на портале'), ('moderation_ok', 'модерация пройдена'), ('moderation_reject', 'модерация отклонена')], max_length=64, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='currency',
            field=models.CharField(blank=True, choices=[('руб.', 'руб.'), ('USD', 'USD'), ('EUR', 'EUR')], help_text='поле необязательное для заполнения', max_length=4, verbose_name='валюта'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='failed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='fall_moderation',
            field=models.TextField(blank=True, help_text='поле необязательное', max_length=254, verbose_name='Сообщение в случае непрохождения модерации вакансии'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
