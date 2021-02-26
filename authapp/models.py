from django.contrib.auth.models import User
from django.db import models


# class Role(models.Model):
#     ROLE_CHOICE = (
#         ('employerapp', 'работодатель'),
#         ('employee', 'соискатель'),
#     )
#     role = models.CharField(verbose_name='статус клиента', max_length=64, choices=ROLE_CHOICE)


class Employer(models.Model):
    company_name = models.CharField(verbose_name='название компании', max_length=128, unique=True)
    tel = models.CharField(verbose_name='телефон', max_length=11, blank=True)
    short_description = models.TextField(verbose_name='краткое описание компании')
    logo = models.ImageField(upload_to='company_logo', blank=True)
    web = models.CharField(verbose_name='вебсайт компании', max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Работодатели'

    def __str__(self):
        return self.company_name


class Seeker(models.Model):
    SEX_CHOICE = (
        ('male', 'мужской'),
        ('female', 'женский')
    )
    MARRIED_STATUS = (
        ('h', 'холост'),
        ('m', 'замужем/женат'),
        ('d', 'разведен/разведена'),
        ('v', 'вдовец/вдова')
    )
    patronimyc = models.CharField(verbose_name='Отчество', max_length=64)
    age = models.PositiveSmallIntegerField(verbose_name='возраст', default=18)
    sex = models.CharField(verbose_name='Ваш пол', max_length=32, choices=SEX_CHOICE)
    married = models.CharField(verbose_name='Семейное положение', max_length=1, choices=MARRIED_STATUS)
    skills = models.TextField(verbose_name='Навыки (знание программ)', max_length=264, blank=True)
    hobby = models.TextField(verbose_name='Ваши увлечения', max_length=264, blank=True)
    tel = models.CharField(verbose_name='телефон', max_length=11, blank=True)
    photo = models.ImageField(upload_to='seeker_photo', blank=True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Соискатели'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.username})'


