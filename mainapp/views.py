from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import UserLoginForm
from authapp.models import Employer
from employerapp.models import Vacancy, FavoriteResumes
from mainapp.models import News
from workerapp.models import Resume, FavoriteVacancies


def main(request):
    title = 'Главная'
    fav_resumes = []
    fav_vacancies = []
    try:
        favorite_resumes = FavoriteResumes.objects.filter(employer=request.user.employer)
        for item in favorite_resumes:
            fav_resumes.append(item.resume.position)
    except AttributeError:
        pass

    try:
        fav_vac = FavoriteVacancies.objects.filter(seeker=request.user.seeker)
        for item in fav_vac:
            fav_vacancies.append(item.vacancy.vacancy_name)
    except AttributeError:
        pass

    news = News.objects.filter(is_active=True).order_by('-published')[:3]
    employers = Employer.objects.filter(status='moderation_ok').order_by('?')[:6]
    vacancies = Vacancy.objects.filter(action='moderation_ok', hide=False).order_by(
        '-published')
    resume = Resume.objects.filter(action='moderation_ok', hide=False).order_by('-published')
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
        'employers': employers,
        'vacancies': vacancies,
        'resume': resume,
        'favorite_resumes': fav_resumes,
        'favorite_vacancies': fav_vacancies
    }
    return render(request, 'mainapp/index.html', context)


def news(request, page=1):
    title = 'Новости'
    news = News.objects.filter(is_active=True).order_by('-published')
    paginator = Paginator(news, 4)
    try:
        news_paginator = paginator.page(page)
    except PageNotAnInteger:
        news_paginator = paginator.page(1)
    except EmptyPage:
        news_paginator = paginator.page(paginator.num_pages)
    context = {
        'title': title,
        'news': news_paginator,
    }
    return render(request, 'mainapp/news.html', context)


def news_detail(request, pk):
    one_news = News.objects.get(pk=pk)
    title = one_news.pk
    url = f'http://127.0.0.1:8000{request.path}'
    context = {
        'title': title,
        'one_news': one_news,
        'url': url
    }
    return render(request, 'mainapp/news_detail.html', context)


def search_news(request):
    title = 'Поиск новостей'
    search = request.GET.get('search')
    search_paginator = None
    if search:
        results = News.objects.filter(Q(title__icontains=search) | Q(description__icontains=search), is_active=True).order_by(
            '-published')

        page = request.GET.get('page')
        paginator = Paginator(results, 4)
        try:
            search_paginator = paginator.page(page)
        except PageNotAnInteger:
            search_paginator = paginator.page(1)
        except EmptyPage:
            search_paginator = paginator.page(paginator.num_pages)

    context = {'title': title, 'object_list': search_paginator}

    return render(request, 'mainapp/search_news.html', context)


@login_required
def add_delete_favorites(request):
    if request.user.employer and request.is_ajax():
        resume_id = request.GET.get('data_id')
        data_class = request.GET.get('class')
        res = Resume.objects.get(pk=resume_id)
        if data_class == 'bi bi-star':
            favorite_resume = FavoriteResumes(employer=request.user.employer, resume=res)
            if not FavoriteResumes.objects.filter(resume=res, employer=request.user.employer).first():
                favorite_resume.save()
        else:
            favorite_resume = FavoriteResumes.objects.get(employer=request.user.employer, resume=res)
            favorite_resume.delete()

        return JsonResponse({})


@login_required
def change_favorites_vacancies(request):
    if request.user.seeker and request.is_ajax():
        vacancy_id = request.GET.get('data_id')
        data_class = request.GET.get('class')
        vac = Vacancy.objects.get(pk=vacancy_id)
        if data_class == 'bi bi-star':
            favorite_vacancy = FavoriteVacancies(seeker=request.user.seeker, vacancy=vac)
            if not FavoriteVacancies.objects.filter(vacancy=vac, seeker=request.user.seeker).first():
                favorite_vacancy.save()
        else:
            favorite_vacancy = FavoriteVacancies.objects.get(seeker=request.user.seeker, vacancy=vac)
            favorite_vacancy.delete()

        return JsonResponse({})
