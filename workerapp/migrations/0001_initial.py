# Generated by Django 3.1.1 on 2021-04-28 23:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authapp', '0013_auto_20210428_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=64, verbose_name='желаемая должность')),
                ('min_salary', models.IntegerField(blank=True, help_text='поле необязательное для заполнения', verbose_name='минимальный уровень з/п')),
                ('max_salary', models.IntegerField(blank=True, help_text='поле необязательное для заполнения', verbose_name='максимальный уровень з/п')),
                ('currency', models.CharField(blank=True, choices=[('руб.', 'руб.'), ('USD', 'USD'), ('EUR', 'EUR')], help_text='поле необязательное для заполнения', max_length=4, verbose_name='валюта')),
                ('published', models.DateField(default=datetime.datetime.now, verbose_name='дата публикации')),
                ('action', models.CharField(choices=[('draft', 'сохранить черновик'), ('publish', 'опубликовать на портале'), ('moderation_ok', 'модерация пройдена'), ('moderation_reject', 'модерация отклонена')], max_length=64, verbose_name='статус')),
                ('hide', models.BooleanField(default=False, verbose_name='резюме удалено / скрыто')),
                ('failed_moderation', models.TextField(blank=True, help_text='поле необязательное', max_length=254, verbose_name='Сообщение в случае непрохождения модерации вакансии')),
                ('seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.seeker')),
            ],
            options={
                'verbose_name_plural': 'Резюме',
            },
        ),
        migrations.CreateModel(
            name='ResumeExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=128, verbose_name='Название компании')),
                ('job_title', models.CharField(max_length=128, verbose_name='Название вакансии')),
                ('start_date', models.DateField(verbose_name='Начало работы')),
                ('finish_date', models.DateField(blank=True, help_text='оставьте пустым если работаете по настоящее время', verbose_name='Конец работы')),
                ('job_description', models.TextField(blank=True, help_text='поле необязательное для заполнения', verbose_name='Описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience', to='workerapp.resume')),
            ],
            options={
                'verbose_name_plural': 'Опыт',
            },
        ),
        migrations.CreateModel(
            name='ResumeEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edu_type', models.CharField(choices=[('high', 'высшее'), ('online', 'онлайн-курсы')], default='high', max_length=32, verbose_name='Тип образования')),
                ('degree', models.CharField(choices=[('master', 'магистр'), ('bachelor', 'бакалавр'), ('specialist', 'специалист'), ('sertificate', 'сертификат')], max_length=64, verbose_name='Квалификация')),
                ('institution_name', models.CharField(max_length=64, verbose_name='Название учреждения')),
                ('from_date', models.DateField(verbose_name='Начало периода')),
                ('to_date', models.DateField(verbose_name='Конец периода(фактическая или планируемая)')),
                ('course_name', models.CharField(max_length=256, verbose_name='Название курса/кафедры')),
                ('edu_description', models.TextField(blank=True, help_text='поле необязательное для заполнения', verbose_name='Описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educationitems', to='workerapp.resume', verbose_name='Резюме')),
            ],
            options={
                'verbose_name_plural': 'Обучение',
            },
        ),
    ]
