# Generated by Django 3.2.3 on 2021-07-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employerapp', '0012_favoriteresumes_is_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='is_favorite',
            field=models.BooleanField(default=False, verbose_name='добавлено в избранное'),
        ),
    ]