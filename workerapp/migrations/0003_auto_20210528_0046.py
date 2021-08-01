# Generated by Django 3.2.3 on 2021-05-28 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workerapp', '0002_auto_20210428_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='failed_moderation',
            field=models.TextField(blank=True, help_text='поле необязательное', max_length=254, verbose_name='Сообщение в случае непрохождения модерации резюме'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='max_salary',
            field=models.CharField(blank=True, help_text='поле необязательное для заполнения', max_length=7, verbose_name='максимальный уровень з/п'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='min_salary',
            field=models.CharField(blank=True, help_text='поле необязательное для заполнения', max_length=7, verbose_name='минимальный уровень з/п'),
        ),
    ]
