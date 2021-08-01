# Generated by Django 3.2.3 on 2021-06-21 04:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workerapp', '0004_alter_resumeexperience_finish_date'),
        ('employerapp', '0008_auto_20210428_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendOffers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='дата направления предложения')),
                ('cover_letter', models.TextField(blank=True, help_text='поле не обязательное', max_length=524, verbose_name='Сопроводительное письмо по предлагаемой вакансии')),
                ('contact_phone', models.CharField(blank=True, help_text='поле не обязательное', max_length=12, verbose_name='конт. тел с кем связываться по вакансии')),
                ('status', models.CharField(choices=[('new', 'новое (не прочитано)'), ('read', 'прочитано')], default='new', max_length=32, verbose_name='статус предложения')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workerapp.resume', verbose_name='предложение для резюме')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employerapp.vacancy', verbose_name='выберите вакансию по которой хотите направить предложение соискателю')),
            ],
            options={
                'verbose_name_plural': 'Предложения для соискателей',
            },
        ),
    ]
