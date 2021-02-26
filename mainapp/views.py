from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import UserLoginForm
from authapp.models import Employer
from mainapp.models import News
from mainapp.templates.mainapp.forms import ContactForm


def main(request):
    title = 'Главная'
    news = News.objects.filter(is_active=True).order_by('-published')[:3]
    employers = Employer.objects.filter(is_active=True).order_by('?')[:12]

    login_form = UserLoginForm(data=request.POST or None)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))
    context = {
        'title': title,
        'news': news,
        'login_form': login_form,
        'employers': employers
    }
    return render(request, 'mainapp/index.html', context)


def news(request):
    title = 'Новости'
    news = News.objects.filter(is_active=True).order_by('-published')
    context = {
        'title': title,
        'news': news,
    }
    return render(request, 'mainapp/news.html', context)


def news_detail(request, pk):
    one_news = News.objects.get(pk=pk)
    title = one_news.pk
    context = {
        'title': title,
        'one_news': one_news
    }
    return render(request, 'mainapp/news_detail.html', context)


def contacts(request):
    title = 'Контакты'
    sent = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            recipients = ['usov.p@mail.ru']

            send_mail('сообщение с сайта IT Recrut',
                      f'от: {name}\nemail: {email}\n{message}', DEFAULT_FROM_EMAIL, recipients)

            sent = True
    else:
        form = ContactForm()
    context = {
        'title': title,
        'sent': sent,
        'form': form
    }
    return render(request, 'mainapp/contacts.html', context)

