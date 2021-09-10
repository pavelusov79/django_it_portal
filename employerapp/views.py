from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from authapp.models import Employer
from employerapp.forms import VacancyCreationForm, VacancyEditForm, SendOfferForm
from employerapp.models import Vacancy, SendOffers, FavoriteResumes
from mainapp.views import change_favorites_vacancies
from workerapp.models import Resume, SendResponse, FavoriteVacancies


@login_required
def employer_cabinet(request, emp_id):
    title = 'Личный кабинет работодателя'
    employer = get_object_or_404(Employer, pk=emp_id)
    vacancies = Vacancy.objects.filter(action='moderation_ok', hide=False,
                                       employer=employer).order_by(
        'published')
    drafts = Vacancy.objects.filter(action='draft', hide=False, employer=employer).order_by(
        'published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    vacancies_all = Vacancy.objects.filter(Q(action='moderation_ok') | Q(
        action='moderation_reject'), employer=employer).exclude(action='draft').exclude(hide=True).order_by('published')
    offers = SendOffers.objects.filter(vacancy__employer=employer.pk).order_by('date')
    take_offers = SendResponse.objects.filter(vacancy__in=vacancies).select_related()
    favorites = FavoriteResumes.objects.filter(employer=employer).order_by('date')
    context = {
        'title': title,
        'vacancies': vacancies,
        'employer': employer,
        'drafts': drafts,
        'vacancies_hide': vacancies_hide,
        'vacancies_all': vacancies_all,
        'offers': offers,
        'take_offers': take_offers,
        'favorites': favorites
    }
    return render(request, 'employerapp/employer_cabinet.html', context)


@login_required
def vacancy_published(request, emp_id):
    title = 'Опубликованные вакансии'
    employer = get_object_or_404(Employer, pk=emp_id)
    vacancies = Vacancy.objects.filter(action='moderation_ok', hide=False,
                                       employer=employer).order_by(
        'published')
    drafts = Vacancy.objects.filter(action='draft', hide=False, employer=employer).order_by(
        'published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    vacancies_all = Vacancy.objects.filter(Q(action='moderation_ok') | Q(
        action='moderation_reject'), employer=employer).exclude(action='draft').exclude(
        hide=True).order_by('published')
    offers = SendOffers.objects.filter(vacancy__employer=employer.pk).order_by('date')
    take_offers = SendResponse.objects.filter(vacancy__in=vacancies).select_related()
    favorites = FavoriteResumes.objects.filter(employer=employer).order_by('date')
    context = {
        'title': title,
        'vacancies': vacancies,
        'employer': employer,
        'drafts': drafts,
        'vacancies_hide': vacancies_hide,
        'vacancies_all': vacancies_all,
        'offers': offers,
        'take_offers': take_offers,
        'favorites': favorites
    }
    return render(request, 'employerapp/vacancy_published.html', context)


@login_required
def creation(request, emp_id):
    employer = get_object_or_404(Employer, pk=emp_id)
    title = 'создание вакансии'
    sent = False
    action = None
    if request.method == 'POST':
        form = VacancyCreationForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.action = form.cleaned_data.get('action')
            vacancy.employer = employer
            vacancy.save()
            sent = True
            action = vacancy.action

    else:
        form = VacancyCreationForm()
    context = {'title': title, 'form': form, 'sent': sent, 'employer': employer, 'action': action}

    return render(request, 'employerapp/vacancy_creation.html', context)


@login_required
def vacancy_edit_draft(request, emp_id, pk):
    title = 'Редактирование вакансии'
    vacancy = get_object_or_404(Vacancy, pk=pk)
    employer = get_object_or_404(Employer, pk=emp_id)
    sent = False
    action = None
    if request.method == 'POST':
        form = VacancyCreationForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            sent = True
            action = vacancy.action
    else:
        form = VacancyCreationForm(instance=vacancy)

    context = {'title': title, 'form': form, 'sent': sent, 'employer': employer, 'vacancy':
        vacancy, 'action': action}

    return render(request, 'employerapp/vacancy_edit.html', context)


@login_required
def vacancy_edit(request, emp_id, pk):
    title = 'Редактирование вакансии'
    vacancy = get_object_or_404(Vacancy, pk=pk)
    employer = get_object_or_404(Employer, pk=emp_id)
    sent = False
    action = None
    if request.method == 'POST':
        form = VacancyEditForm(request.POST, instance=vacancy)
        vacancy.action = 'publish'
        vacancy.fall_moderation = ''
        form.save()
        vacancy.save()
        sent = True
    else:
        form = VacancyEditForm(instance=vacancy)

    context = {'title': title, 'form': form, 'sent': sent, 'employer': employer, 'vacancy':
        vacancy, 'action': action}

    return render(request, 'employerapp/vacancy_edit.html', context)


@login_required
def vacancy_delete(request, emp_id, pk):
    title = 'Удаление вакансии'
    employer = get_object_or_404(Employer, pk=emp_id)
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if request.method == 'POST' and (vacancy.action == 'draft' or vacancy.action ==
                                     'moderation_ok'):
        if not vacancy.hide:
            vacancy.hide = True
        else:
            vacancy.hide = False
        vacancy.save()
        return HttpResponseRedirect(reverse('employer:cabinet', args=[vacancy.employer.pk]))

    context = {'title': title, 'vacancy_delete': vacancy, 'employer': employer}

    return render(request, 'employerapp/vacancy_delete.html', context)


@login_required
def vacancy_draft(request, emp_id):
    employer = get_object_or_404(Employer, pk=emp_id)
    title = 'Черновики'
    drafts = Vacancy.objects.filter(action='draft', hide=False, employer=employer).order_by('published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    vacancies = Vacancy.objects.filter(action='moderation_ok', hide=False,
                                       employer=employer).order_by(
        'published')
    vacancies_all = Vacancy.objects.filter(Q(action='moderation_ok') | Q(
        action='moderation_reject'), employer=employer).exclude(action='draft').exclude(
        hide=True).order_by('published')
    offers = SendOffers.objects.filter(vacancy__employer=employer.pk).order_by('date')
    take_offers = SendResponse.objects.filter(vacancy__in=vacancies).select_related()
    favorites = FavoriteResumes.objects.filter(employer=employer).order_by('date')
    context = {
        'title': title,
        'employer': employer,
        'drafts': drafts,
        'vacancies_hide': vacancies_hide,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'offers': offers,
        'take_offers': take_offers,
        'favorites': favorites
    }

    return render(request, 'employerapp/vacancy_drafts.html', context)


@login_required
def vacancy_hide(request, emp_id):
    employer = get_object_or_404(Employer, pk=emp_id)
    title = 'Удаленные вакансии'
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    drafts = Vacancy.objects.filter(action='draft', hide=False, employer=employer).order_by(
        'published')
    vacancies = Vacancy.objects.filter(action='moderation_ok', hide=False,
                                       employer=employer).order_by(
        'published')
    vacancies_all = Vacancy.objects.filter(Q(action='moderation_ok') | Q(
        action='moderation_reject'), employer=employer).exclude(action='draft').exclude(
        hide=True).order_by('published')
    offers = SendOffers.objects.filter(vacancy__employer=employer.pk).order_by('date')
    take_offers = SendResponse.objects.filter(vacancy__in=vacancies).select_related()
    favorites = FavoriteResumes.objects.filter(employer=employer).order_by('date')
    context = {
        'title': title,
        'employer': employer,
        'vacancies_hide': vacancies_hide,
        'drafts': drafts,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'offers': offers,
        'take_offers': take_offers,
        'favorites': favorites
    }

    return render(request, 'employerapp/vacancy_hide.html', context)


@login_required
def messages(request, emp_id):
    title = 'Сообщения от админа портала'
    employer = get_object_or_404(Employer, pk=emp_id)
    vacancies_all = Vacancy.objects.filter(Q(action='moderation_ok') | Q(
        action='moderation_reject'), employer=employer).exclude(action='draft').exclude(
        hide=True).order_by('published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    drafts = Vacancy.objects.filter(action='draft', hide=False, employer=employer).order_by('published')
    vacancies = Vacancy.objects.filter(action='moderation_ok', hide=False,
                                       employer=employer).order_by(
        'published')
    offers = SendOffers.objects.filter(vacancy__employer=employer.pk).order_by('date')
    take_offers = SendResponse.objects.filter(vacancy__in=vacancies).select_related()
    favorites = FavoriteResumes.objects.filter(employer=employer).order_by('date')

    context = {
        'title': title,
        'employer': employer,
        'vacancies_hide': vacancies_hide,
        'drafts': drafts,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'offers': offers,
        'take_offers': take_offers,
        'favorites': favorites
    }

    return render(request, 'employerapp/employer_messages.html', context)


@login_required
def vacancy_view(request, emp_id, pk):
    title = 'Вакансия'
    vacancy = get_object_or_404(Vacancy, pk=pk)
    employer = get_object_or_404(Employer, pk=emp_id)
    favorite = FavoriteVacancies.objects.filter(vacancy=vacancy, seeker=request.user.seeker).first()
    if request.is_ajax() and request.user.seeker:
        change_favorites_vacancies(request)

    context = {'title': title, 'item': vacancy, 'employer': employer, 'favorite': favorite}

    return render(request, 'employerapp/vacancy_view.html', context)


@login_required
def offer_ajax(request):
    if request.user.seeker and request.is_ajax():
        vacancy_id = request.GET.get('vacancy_id')
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        send_offer = SendOffers.objects.get(vacancy=vacancy)
        status_id = request.GET.get('status_id')
        if status_id == 'новое (не прочитано)':
            send_offer.status = SendOffers.READ
            send_offer.save()
            return send_offer


@login_required
def send_offer(request, emp_id, pk):
    title = 'Предложение по работе'
    employer = get_object_or_404(Employer, pk=emp_id)
    resume = get_object_or_404(Resume, pk=pk)

    sent = False
    if request.method == 'POST':
        form = SendOfferForm(request.POST, employer=employer)
        send = SendOffers()

        if form.is_valid():
            send.vacancy = form.cleaned_data.get('vacancy')
            send.cover_letter = form.cleaned_data.get('cover_letter')
            send.contact_phone = form.cleaned_data.get('contact_phone')
            send.resume = resume
            send.save()
            sent = True
    else:
        form = SendOfferForm(employer=employer)

    context = {'title': title, 'employer': employer, 'sent': sent, 'form': form}

    return render(request, 'employerapp/send_offer.html',  context)


@login_required
def send_offers(request, emp_id):
    title = 'Направленные предложения'
    employer = get_object_or_404(Employer, pk=emp_id)
    vacancies_all = Vacancy.objects.filter(Q(action='moderation_ok') | Q(
        action='moderation_reject'), employer=employer).exclude(action='draft').exclude(
        hide=True).order_by('published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    drafts = Vacancy.objects.filter(action='draft', hide=False, employer=employer).order_by('published')
    vacancies = Vacancy.objects.filter(action='moderation_ok', hide=False,
                                       employer=employer).order_by(
        'published')
    offers = SendOffers.objects.filter(vacancy__employer=employer.pk).order_by('date')
    take_offers = SendResponse.objects.filter(vacancy__in=vacancies).select_related()
    favorites = FavoriteResumes.objects.filter(employer=employer).order_by('date')
    context = {
        'title': title,
        'employer': employer,
        'vacancies_hide': vacancies_hide,
        'drafts': drafts,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'offers': offers,
        'take_offers': take_offers,
        'favorites': favorites
    }

    return render(request, 'employerapp/employer_offers.html', context)


@login_required
def my_offers(request, emp_id):
    title = 'Отклики по вакансиям'
    employer = get_object_or_404(Employer, pk=emp_id)
    vacancies = Vacancy.objects.filter(action='moderation_ok', hide=False,
                                       employer=employer).order_by('published')
    vacancies_all = Vacancy.objects.filter(Q(action='moderation_ok') | Q(
        action='moderation_reject'), employer=employer).exclude(action='draft').exclude(
        hide=True).order_by('published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    drafts = Vacancy.objects.filter(action='draft', hide=False, employer=employer).order_by('published')
    offers = SendOffers.objects.filter(vacancy__employer=employer.pk).order_by('date')
    favorites = FavoriteResumes.objects.filter(employer=employer).order_by('date')
    take_offers = SendResponse.objects.filter(vacancy__in=vacancies).select_related()
    context = {
        'title': title,
        'employer': employer,
        'vacancies_hide': vacancies_hide,
        'drafts': drafts,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'offers': offers,
        'take_offers': take_offers,
        'favorites': favorites
    }
    return render(request, 'employerapp/offers_list.html', context)


def company_profile(request, emp_id):
    title = 'Профиль компании'
    employer = get_object_or_404(Employer, pk=emp_id)
    vacancies = Vacancy.objects.filter(action='moderation_ok', hide=False,
                                       employer=employer).order_by('published')
    context = {'title': title, 'employer': employer, 'vacancies': vacancies}

    return render(request, 'employerapp/company_profile.html', context)


@login_required
def favorites_resume(request, emp_id):
    title = 'Избранные резюме'
    employer = get_object_or_404(Employer, pk=emp_id)
    vacancies = Vacancy.objects.filter(action='moderation_ok', hide=False,
                                       employer=employer).order_by('published')
    take_offers = SendResponse.objects.filter(vacancy__in=vacancies).select_related()
    vacancies_all = Vacancy.objects.filter(Q(action='moderation_ok') | Q(
        action='moderation_reject'), employer=employer).exclude(action='draft').exclude(
        hide=True).order_by('published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    drafts = Vacancy.objects.filter(action='draft', hide=False, employer=employer).order_by('published')
    offers = SendOffers.objects.filter(vacancy__employer=employer.pk).order_by('date')
    favorites = FavoriteResumes.objects.filter(employer=employer).order_by('date')
    context = {
        'title': title,
        'employer': employer,
        'vacancies_hide': vacancies_hide,
        'drafts': drafts,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'offers': offers,
        'take_offers': take_offers,
        'favorites': favorites
    }

    return render(request, 'employerapp/favorites.html', context)


@login_required
def delete_favorite(request, emp_id, pk):
    title = 'Удаление избранных резюме'
    employer = get_object_or_404(Employer, pk=emp_id)
    favorite = get_object_or_404(FavoriteResumes, pk=pk)

    if request.method == 'POST':
        favorite.delete()
        return HttpResponseRedirect(reverse('employer:favorites', args=[employer.pk]))

    context = {'title': title, 'favorite': favorite, 'employer': employer}

    return render(request, 'employerapp/delete_favorite.html', context)


@login_required
def search_resume(request, emp_id):
    title = 'Поиск резюме'
    employer = get_object_or_404(Employer, pk=emp_id)
    search = request.GET.get('search')
    city = request.GET.get('city')
    salary = request.GET.get('salary')
    currency = request.GET.get('currency')
    gender = request.GET.get('gender')
    from_date = request.GET.get('from_date')
    till_date = request.GET.get('till_date')
    results = None
    fav_resume = []
    if search or city or gender or salary or from_date or till_date:
        favorite_resumes = FavoriteResumes.objects.filter(employer=employer)
        for item in favorite_resumes:
            fav_resume.append(item.resume.position)
    if search:
        results = Resume.objects.filter(Q(position__icontains=search) | Q(skills__icontains=search)).filter(action='moderation_ok', hide=False).order_by('-published')

    if city:
        if results:
            results = results.filter(seeker__city=city)
        else:
            results = Resume.objects.filter(seeker__city=city, action='moderation_ok', hide=False).order_by('-published')

    if gender == 'female' or gender == 'male':
        if results:
            results = results.filter(seeker__sex=gender)
        else:
            results = Resume.objects.filter(seeker__sex=gender, action='moderation_ok', hide=False).order_by('-published')

    if salary:
        if results:
            results = results.filter(min_salary__lte=salary, currency=currency)
        else:
            results = Resume.objects.filter(min_salary__lte=salary, currency=currency, action='moderation_ok', hide=False).order_by('-published')

    if from_date:
        if results:
            results = results.filter(published__gte=from_date)
        else:
            results = Resume.objects.filter(published__gte=from_date, action='moderation_ok', hide=False).order_by('-published')

    if till_date:
        if results:
            results = results.filter(published__lte=till_date)
        else:
            results = Resume.objects.filter(published__lte=till_date, action='moderation_ok', hide=False).order_by('-published')
    print('fav_resume_search = ', fav_resume)
    page = request.GET.get('page')
    paginator = Paginator(results, 1)
    try:
        search_paginator = paginator.page(page)
    except PageNotAnInteger:
        search_paginator = paginator.page(1)
    except EmptyPage:
        search_paginator = paginator.page(paginator.num_pages)

    context = {'title': title, 'object_list': search_paginator, 'employer': employer, 'fav_list': fav_resume}

    return render(request, 'employerapp/search_resume.html', context)