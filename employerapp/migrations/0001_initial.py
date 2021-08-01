# Generated by Django 3.1.1 on 2021-03-09 00:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacancy_name', models.CharField(max_length=128, verbose_name='название вакансии')),
                ('city', models.CharField(max_length=64, verbose_name='город')),
                ('salary', models.CharField(blank=True, help_text='поле необязательное для заполнения', max_length=64, verbose_name='уровень з/п')),
                ('description', models.TextField(max_length=264, verbose_name='описание / обязанности')),
                ('requirements', models.TextField(max_length=264, verbose_name='требования к кандидату')),
                ('published', models.DateField(default=datetime.datetime.now, verbose_name='дата публикации')),
                ('contact_person', models.CharField(max_length=128, verbose_name='контактное лицо')),
                ('contact_email', models.EmailField(blank=True, help_text='поле необязательное', max_length=254, verbose_name='контактная почта')),
                ('is_active', models.BooleanField(default=False, verbose_name='вакансия опубликована')),
                ('hide', models.BooleanField(default=False, verbose_name='вакансия удалена / скрыта')),
                ('action', models.CharField(choices=[('draft', 'сохранить черновик'), ('publish', 'опубликовать на портале')], max_length=64, verbose_name='статус')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.employer')),
            ],
            options={
                'verbose_name_plural': 'Вакансии',
            },
        ),
    ]