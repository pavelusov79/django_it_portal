from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class Employer(models.Model):
    NEED_MODER = 'need_moderation'
    MODER_OK = 'moderation_ok'
    MODER_REJECT = 'moderation_reject'
    EMPLOYER_STATUS_CHOICES = (
        (NEED_MODER, 'требуется модерация'),
        (MODER_OK, 'модерация пройдена успешно'),
        (MODER_REJECT, 'отклонено модератором')
    )
    company_name = models.CharField(verbose_name='название компании', max_length=128, unique=True)
    city = models.CharField(verbose_name='город', max_length=64, blank=True)
    tel = models.CharField(verbose_name='телефон', max_length=11, blank=True)
    short_description = models.TextField(verbose_name='краткое описание компании')
    logo = models.ImageField(upload_to='company_logo', blank=True)
    web = models.CharField(verbose_name='вебсайт компании', max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(verbose_name='статус компании на сайте',
                              choices=EMPLOYER_STATUS_CHOICES, default=NEED_MODER,
                              max_length=32)
    failed_moderation = models.CharField(max_length=512, blank=True, verbose_name='поле '
                                                                                  'заполняется в случае отклонения модерации')
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(datetime.now() + timedelta(hours=24)))

    def is_activation_key_expired(self):
        if datetime.now() > self.activation_key_expires:
            return True
        else:
            return False

    class Meta:
        verbose_name_plural = 'Работодатели'

    def __str__(self):
        return self.company_name


class Seeker(models.Model):
    NEED_MODER = 'need_moderation'
    MODER_OK = 'moderation_ok'
    MODER_REJECT = 'moderation_reject'
    SEEKER_STATUS_CHOICES = (
        (NEED_MODER, 'требуется модерация'),
        (MODER_OK, 'модерация пройдена успешно'),
        (MODER_REJECT, 'отклонено модератором')
    )
    SEX_CHOICE = (
        ('male', 'мужской'),
        ('female', 'женский')
    )
    MARRIED_STATUS = (
        ('h', 'холост'),
        ('m', 'в браке'),
        ('d', 'в разводе')
    )
    patronimyc = models.CharField(verbose_name='Отчество', max_length=64)
    age = models.PositiveSmallIntegerField(verbose_name='возраст', default=18)
    sex = models.CharField(verbose_name='Ваш пол', max_length=32, choices=SEX_CHOICE)
    married = models.CharField(verbose_name='Семейное положение', max_length=1, choices=MARRIED_STATUS)
    city = models.CharField(verbose_name='город', max_length=64, blank=True)
    skills = models.TextField(verbose_name='Навыки (знание программ)', max_length=264, blank=True)
    hobby = models.TextField(verbose_name='Ваши увлечения', max_length=264, blank=True)
    tel = models.CharField(verbose_name='телефон', max_length=11, blank=True)
    photo = models.ImageField(upload_to='seeker_photo', blank=True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(verbose_name='статус соискателя на сайте',
                              choices=SEEKER_STATUS_CHOICES, default=NEED_MODER, max_length=32)
    failed_moderation = models.CharField(max_length=512, blank=True, verbose_name='поле '
                                                                                  'заполняется в случае отклонения модерации')
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(datetime.now() + timedelta(hours=24)))

    def is_activation_key_expired(self):
        if datetime.now() > self.activation_key_expires:
            return True
        else:
            return False

    class Meta:
        verbose_name_plural = 'Соискатели'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.username})'


