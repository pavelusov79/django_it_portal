from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from authapp.models import Employer
from employerapp.models import Vacancy


class AuthappTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='company1', password='geekbrains', email='company1@mail.ru')
        Employer.objects.create(company_name='Super Company', short_description='Lorem', user=self.user,
                                                city='Moscow', tel='89147903322')
        emp = Employer.objects.get(id=1)
        emp.status = Employer.MODER_OK
        emp.save()
        Vacancy.objects.create(vacancy_name='Junior developer', city='Moscow', description='lorem',
                                         requirements='lorem', contact_person='Ivanov', action='moderation_ok',
                                         employer=emp)

    def test_create_employer(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)

    def test_employer_cabinet_url(self):
        auth = self.client.login(username=self.user.username, password=self.user.password)
        if auth:
            response = self.client.get('/employer/1/')
            self.assertEqual(response.status_code, 200)

    def test_create_vacancy(self):
        auth = self.client.login(username=self.user.username, password=self.user.password)
        if auth:
            response = self.client.get('/employer/1/vacancy_create/')
            self.assertEqual(response.status_code, 200)

    def test_vacancy_view_url(self):
        auth = self.client.login(username=self.user.username, password=self.user.password)
        if auth:
            response = self.client.get('/employer/1/vacancy_view/1/')
            self.assertEqual(response.status_code, 200)


