from datetime import datetime

from django.db import models

from authapp.models import Seeker


class Resume(models.Model):
    RESUME_ACTION_CHOICE = (
        ('draft', 'сохранить черновик'),
        ('publish', 'опубликовать на портале'),
        ('moderation_ok', 'модерация пройдена'),
        ('moderation_reject', 'модерация отклонена')
    )
    RUB = 'руб.'
    USD = 'USD'
    EUR = 'EUR'
    CURRENCY_CHOICE = (
        (RUB, 'руб.'),
        (USD, 'USD'),
        (EUR, 'EUR')
    )
    position = models.CharField(max_length=64, verbose_name='желаемая должность')
    min_salary = models.CharField(verbose_name='минимальный уровень з/п', max_length=7, blank=True,
                                  help_text='поле необязательное для заполнения')
    max_salary = models.CharField(verbose_name='максимальный уровень з/п', max_length=7, blank=True,
                                  help_text='поле необязательное для заполнения')
    currency = models.CharField(verbose_name='валюта', max_length=4, blank=True,
                                choices=CURRENCY_CHOICE, help_text='поле необязательное для '
                                                                   'заполнения')
    published = models.DateField(verbose_name='дата публикации', default=datetime.now)
    skills = models.TextField(verbose_name='Ключевые навыки', max_length=512, blank=True)
    hobby = models.TextField(verbose_name='Ваши увлечения', max_length=512, blank=True,
                             help_text='поле необязательно для заполнения')
    action = models.CharField(verbose_name='статус', max_length=64, choices=RESUME_ACTION_CHOICE)
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    hide = models.BooleanField(verbose_name='резюме удалено / скрыто', default=False)
    failed_moderation = models.TextField(verbose_name='Сообщение в случае непрохождения '
        'модерации резюме', max_length=254, blank=True, help_text='поле необязательное')
    is_favorite = models.BooleanField(verbose_name='добавлен в избранное', default=False)

    def __str__(self):
        return f'{self.position} ({self.seeker.user.first_name} {self.seeker.user.last_name} ' \
               f'{self.seeker.patronimyc})'

    class Meta:
        verbose_name_plural = 'Резюме'

    def save(self, *args, **kwargs):
        if self.action == 'moderation_ok' and self.seeker.user.is_superuser or self.action == 'moderation_reject':
            self.published = datetime.now()
        super(Resume, self).save(*args, **kwargs)

    def get_experience_items(self):
        return self.experience.select_related().filter(is_active=True)

    def get_education_items(self):
        return self.educationitems.select_related().filter(is_active=True)


class ResumeEducation(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='Резюме', related_name='educationitems')
    HIGH = 'high'
    ONLINE = 'online'
    EDU_TYPE_CHOICES = (
        ('high', 'высшее'),
        ('online', 'онлайн-курсы'),
    )
    edu_type = models.CharField(verbose_name='Тип образования', max_length=32, choices=EDU_TYPE_CHOICES, blank=False, default=HIGH)
    MASTER = 'master'
    BACHELOR = 'bachelor'
    SPECIALIST = 'specialist'
    SERTIFICATE = 'sertificate'
    DEGREE_CHOICES = (
        (MASTER, 'магистр'),
        (BACHELOR, 'бакалавр'),
        (SPECIALIST, 'специалист'),
        (SERTIFICATE, 'сертификат'),
    )
    degree = models.CharField(verbose_name='Квалификация', max_length=64, choices=DEGREE_CHOICES)
    institution_name = models.CharField(verbose_name='Название учреждения', max_length=64)
    from_date = models.DateField(verbose_name='Начало периода')
    to_date = models.DateField(verbose_name='Конец периода(фактическая или планируемая)')
    course_name = models.CharField(verbose_name='Название курса/кафедры', max_length=256)
    edu_description = models.TextField(verbose_name='Описание', blank=True, help_text='поле '
            'необязательное для заполнения')
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    class Meta:
        verbose_name_plural = 'Обучение'

    def __str__(self):
        return f'{self.resume.position} ({self.resume.seeker.user.first_name}' \
               f' {self.resume.seeker.user.last_name})'


class ResumeExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience')
    company_name = models.CharField(verbose_name='Название компании', max_length=128)
    job_title = models.CharField(verbose_name='Название вакансии', max_length=128)
    start_date = models.DateField(verbose_name='Начало работы')
    finish_date = models.DateField(verbose_name='Конец работы', blank=True, null=True,
                               help_text='оставьте пустым если работаете по настоящее время')
    job_description = models.TextField(verbose_name='Описание', blank=True, help_text='поле '
            'необязательное для заполнения')
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    class Meta:
        verbose_name_plural = 'Опыт'

    def __str__(self):
        return f'{self.resume.position} ({self.resume.seeker.user.first_name}' \
               f' {self.resume.seeker.user.last_name})'


class SendResponse(models.Model):
    NEW = 'new'
    READ = 'read'
    RESPONSE_STATUS = (
        (NEW, 'новое (не прочитано)'),
        (READ, 'прочитано'),
    )
    date = models.DateField(verbose_name='дата направления отклика', default=datetime.now)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='выберите резюме, которое вы хотите'
                                                                              ' направить работодателю')
    vacancy = models.ForeignKey('employerapp.Vacancy', on_delete=models.CASCADE, verbose_name='отклик на вакансию')
    cover_letter = models.TextField(verbose_name='Сопроводительное письмо', blank=True, max_length=524,
                                    help_text='поле не обязательное')
    status = models.CharField(verbose_name='статус направленного отклика на вакансию', max_length=32, choices=RESPONSE_STATUS, default=NEW)

    class Meta:
        verbose_name_plural = 'Направленные отклики на размещенные вакансии'

    def __str__(self):
        return f'{self.resume.position} (на вакансию {self.vacancy.vacancy_name})'


class FavoriteVacancies(models.Model):
    date = models.DateField(verbose_name='дата добавления в избранное', default=datetime.now)
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    vacancy = models.ForeignKey('employerapp.Vacancy', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Избранные вакансии'

    def __str__(self):
        return f'{self.seeker.user.first_name} {self.seeker.user.last_name} ({self.vacancy.vacancy_name})'
