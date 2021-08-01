from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from authapp.models import Seeker
from employerapp.models import Vacancy, SendOffers, FavoriteResumes
from mainapp.views import add_delete_favorites
from workerapp.forms import ResumeEducationForm, ResumeExperienceForm, ResumeForm, SendResponseForm
from workerapp.models import ResumeExperience, ResumeEducation, Resume, SendResponse, FavoriteVacancies


@login_required
def worker_cabinet(request, seeker_id):
    title = 'Личный кабинет соискателя'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resumes_all = Resume.objects.filter(Q(action='moderation_ok') | Q(action='moderation_reject'),
                                        seeker=seeker).exclude(action='draft').exclude(hide=True).order_by('published')
    resumes = Resume.objects.filter(action='moderation_ok', hide=False, seeker=seeker).order_by('published')
    drafts = Resume.objects.filter(action='draft', hide=False, seeker=seeker).order_by('published')
    resumes_hide = Resume.objects.filter(hide=True, seeker=seeker).order_by('published')
    responses = SendOffers.objects.filter(resume__in=resumes).select_related()
    send_resp = SendResponse.objects.filter(resume__seeker=seeker.id).order_by('date')
    favorite_vacancies = FavoriteVacancies.objects.filter(seeker=seeker).order_by('-date')

    context = {'title': title, 'seeker': seeker, 'drafts': drafts, 'resumes_hide': resumes_hide, 'resumes': resumes,
               'resumes_all': resumes_all, 'responses': responses, 'send_resp': send_resp, 'favorites': favorite_vacancies}

    return render(request, 'workerapp/worker_cabinet.html', context)


@login_required
def messages(request, seeker_id):
    title = 'Сообщения от админа портала'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resumes = Resume.objects.filter(action='moderation_ok', hide=False, seeker=seeker).order_by('published')
    resumes_all = Resume.objects.filter(Q(action='moderation_ok') | Q(action='moderation_reject'),
                                        seeker=seeker).exclude(action='draft').exclude(hide=True).order_by('published')
    drafts = Resume.objects.filter(action='draft', hide=False, seeker=seeker).order_by('published')
    resumes_hide = Resume.objects.filter(hide=True, seeker=seeker).order_by('published')
    responses = SendOffers.objects.filter(resume__in=resumes).select_related()
    send_resp = SendResponse.objects.filter(resume__seeker=seeker.id).order_by('date')
    favorite_vacancies = FavoriteVacancies.objects.filter(seeker=seeker).order_by('-date')

    context = {'title': title, 'seeker': seeker, 'drafts': drafts, 'resumes_hide': resumes_hide, 'resumes': resumes,
               'resumes_all': resumes_all, 'responses': responses, 'send_resp': send_resp, 'favorites': favorite_vacancies}

    return render(request, 'workerapp/worker_messages.html', context)


@login_required
def hide_resumes(request, seeker_id):
    title = 'Удаленные/скрытые резюме'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resumes = Resume.objects.filter(action='moderation_ok', hide=False, seeker=seeker).order_by('published')
    resumes_all = Resume.objects.filter(Q(action='moderation_ok') | Q(action='moderation_reject'),
                                        seeker=seeker).exclude(action='draft').exclude(hide=True).order_by('published')
    drafts = Resume.objects.filter(action='draft', hide=False, seeker=seeker).order_by('published')
    resumes_hide = Resume.objects.filter(hide=True, seeker=seeker).order_by('published')
    responses = SendOffers.objects.filter(resume__in=resumes).select_related()
    send_resp = SendResponse.objects.filter(resume__seeker=seeker.id).order_by('date')
    favorite_vacancies = FavoriteVacancies.objects.filter(seeker=seeker).order_by('-date')

    context = {'title': title, 'seeker': seeker, 'drafts': drafts, 'resumes_hide': resumes_hide, 'resumes': resumes,
               'resumes_all': resumes_all, 'responses': responses, 'send_resp': send_resp, 'favorites': favorite_vacancies}

    return render(request, 'workerapp/resume_hide.html', context)


@login_required
def resume_drafts(request, seeker_id):
    title = 'Черновики резюме'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resumes = Resume.objects.filter(action='moderation_ok', hide=False, seeker=seeker).order_by('published')
    resumes_all = Resume.objects.filter(Q(action='moderation_ok') | Q(action='moderation_reject'),
                                        seeker=seeker).exclude(action='draft').exclude(hide=True).order_by('published')
    drafts = Resume.objects.filter(action='draft', hide=False, seeker=seeker).order_by('published')
    resumes_hide = Resume.objects.filter(hide=True, seeker=seeker).order_by('published')
    responses = SendOffers.objects.filter(resume__in=resumes).select_related()
    send_resp = SendResponse.objects.filter(resume__seeker=seeker.id).order_by('date')
    favorite_vacancies = FavoriteVacancies.objects.filter(seeker=seeker).order_by('-date')

    context = {'title': title, 'seeker': seeker, 'drafts': drafts, 'resumes_hide': resumes_hide, 'resumes': resumes,
               'resumes_all': resumes_all, 'responses': responses, 'send_resp': send_resp, 'favorites': favorite_vacancies}

    return render(request, 'workerapp/resume_drafts.html', context)


@login_required
def resume_published(request, seeker_id):
    title = 'Опубликованные резюме'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resumes = Resume.objects.filter(action='moderation_ok', hide=False, seeker=seeker).order_by('published')
    resumes_all = Resume.objects.filter(Q(action='moderation_ok') | Q(action='moderation_reject'),
                                        seeker=seeker).exclude(action='draft').exclude(hide=True).order_by('published')
    drafts = Resume.objects.filter(action='draft', hide=False, seeker=seeker).order_by('published')
    resumes_hide = Resume.objects.filter(hide=True, seeker=seeker).order_by('published')
    responses = SendOffers.objects.filter(resume__in=resumes).select_related()
    send_resp = SendResponse.objects.filter(resume__seeker=seeker.id).order_by('date')
    favorite_vacancies = FavoriteVacancies.objects.filter(seeker=seeker).order_by('-date')

    context = {'title': title, 'seeker': seeker, 'drafts': drafts, 'resumes_hide': resumes_hide, 'resumes': resumes,
               'resumes_all': resumes_all, 'responses': responses, 'send_resp': send_resp, 'favorites': favorite_vacancies}

    return render(request, 'workerapp/resume_published.html', context)


@login_required
def favorites(request, seeker_id):
    title = 'Избранные вакансии'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resumes = Resume.objects.filter(action='moderation_ok', hide=False, seeker=seeker).order_by('published')
    resumes_all = Resume.objects.filter(Q(action='moderation_ok') | Q(action='moderation_reject'),
                                        seeker=seeker).exclude(action='draft').exclude(hide=True).order_by('published')
    drafts = Resume.objects.filter(action='draft', hide=False, seeker=seeker).order_by('published')
    resumes_hide = Resume.objects.filter(hide=True, seeker=seeker).order_by('published')
    responses = SendOffers.objects.filter(resume__in=resumes).select_related()
    send_resp = SendResponse.objects.filter(resume__seeker=seeker.id).order_by('date')
    favorite_vacancies = FavoriteVacancies.objects.filter(seeker=seeker).order_by('-date')

    context = {'title': title, 'seeker': seeker, 'drafts': drafts, 'resumes_hide': resumes_hide, 'resumes': resumes,
               'resumes_all': resumes_all, 'responses': responses, 'send_resp': send_resp, 'favorites': favorite_vacancies}

    return render(request, 'workerapp/favorites.html', context)


@login_required
def create_resume(request, seeker_id):
    title = 'Создание резюме'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resume = None
    experience = ResumeExperience.objects.filter(resume=resume, is_active=True)
    education = ResumeEducation.objects.filter(resume=resume, is_active=True)
    sent = False
    status = None
    education_formset = modelformset_factory(ResumeEducation, form=ResumeEducationForm)
    experience_formset = modelformset_factory(ResumeExperience, form=ResumeExperienceForm)

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        education_form = education_formset(request.POST, prefix='1', queryset=education)
        experience_form = experience_formset(request.POST, prefix='2', queryset=experience)
        if form.is_valid() and education_form.is_valid() and experience_form.is_valid():
            resume = form.save(commit=False)
            resume.seeker = seeker
            resume.action = form.cleaned_data.get('action')
            resume.save()
            for form in education_form:
                education = form.save(commit=False)
                education.edu_type = form.cleaned_data.get('edu_type')
                education.resume = resume
                if education.edu_type:
                    education.save()
            for form in experience_form:
                experience = form.save(commit=False)
                experience.company_name = form.cleaned_data.get('company_name')
                experience.resume = resume
                if experience.company_name:
                    experience.save()

            sent = True
            status = resume.action
    else:
        form = ResumeForm()
        education_form = education_formset(prefix='1', queryset=education)
        experience_form = experience_formset(prefix='2', queryset=experience)

    context = {'title': title, 'sent': sent, 'status': status, 'form': form, 'seeker':
        seeker, 'education_form': education_form, 'experience_form': experience_form,
               'resume': resume, 'experience': experience}
    return render(request, 'workerapp/resume_creation.html', context)


@login_required
def resume_update(request, seeker_id, pk):
    title = 'Редактирование резюме'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resume = get_object_or_404(Resume, pk=pk)
    education = ResumeEducation.objects.filter(resume=resume, is_active=True)
    experience = ResumeExperience.objects.filter(resume=resume, is_active=True)
    education_formset = modelformset_factory(ResumeEducation, form=ResumeEducationForm)
    experience_formset = modelformset_factory(ResumeExperience, form=ResumeExperienceForm)
    sent = False
    status = None
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        education_form = education_formset(request.POST, prefix='1', queryset=education)
        experience_form = experience_formset(request.POST, prefix='2', queryset=experience)
        if form.is_valid() and education_form.is_valid() and experience_form.is_valid():
            form.save()
            for form in education_form:
                education = form.save(commit=False)
                education.resume = resume
                education.edu_type = form.cleaned_data.get('edu_type')
                if education.edu_type:
                    education.save()
            for form in experience_form:
                experience = form.save(commit=False)
                experience.company_name = form.cleaned_data.get('company_name')
                experience.resume = resume
                if experience.company_name:
                    experience.save()

            resume.failed_moderation = ''
            resume.save()
            sent = True
            status = resume.action
    else:
        form = ResumeForm(instance=resume)
        education_form = education_formset(prefix='1', queryset=education)
        experience_form = experience_formset(prefix='2', queryset=experience)
    context = {'title': title, 'seeker': seeker, 'resume': resume, 'sent': sent, 'status': status, 'form': form,
               'education_form': education_form, 'experience_form': experience_form, 'experience': experience}
    return render(request, 'workerapp/resume_creation.html', context)


@login_required
def resume_delete(request, seeker_id, pk):
    title = 'Удаление резюме'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resume = get_object_or_404(Resume, pk=pk)
    if request.method == 'POST' and (resume.action == 'draft' or resume.action == 'moderation_ok'):
        if not resume.hide:
            resume.hide = True
        else:
            resume.hide = False
        resume.save()
        return HttpResponseRedirect(reverse('worker:seeker_cabinet', args=[resume.seeker.pk]))

    context = {'title': title, 'resume_delete': resume, 'seeker': seeker}

    return render(request, 'workerapp/resume_delete.html', context)


@login_required
def resume_experience_delete(request, seeker_id, resume_id, pk):
    title = 'Удаление записи об опыте из резюме'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resume = get_object_or_404(Resume, pk=resume_id)
    experience = get_object_or_404(ResumeExperience, resume=resume, pk=pk)
    if request.method == 'POST':
        if experience.is_active:
            experience.delete()
            if resume.action == 'draft':
                return HttpResponseRedirect(reverse('worker:drafts', args=[seeker.pk]))
            else:
                return HttpResponseRedirect(reverse('worker:published', args=[seeker.pk]))
    context = {'title': title, 'resume': resume, 'seeker': seeker, 'experience': experience}

    return render(request, 'workerapp/resume_experience_delete.html', context)


@login_required
def resume_education_delete(request, seeker_id, resume_id, pk):
    title = 'Удаление записи об образовании из резюме'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resume = get_object_or_404(Resume, pk=resume_id)
    education = get_object_or_404(ResumeEducation, resume=resume, pk=pk)
    if request.method == 'POST':
        if education.is_active:
            education.delete()
            if resume.action == 'draft':
                return HttpResponseRedirect(reverse('worker:drafts', args=[seeker.pk]))
            else:
                return HttpResponseRedirect(reverse('worker:published', args=[seeker.pk]))
    context = {'title': title, 'resume': resume, 'seeker': seeker, 'education': education}

    return render(request, 'workerapp/resume_education_delete.html', context)


@login_required
def resume_view(request, seeker_id, pk):
    title = "Резюме"
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resume = Resume.objects.get(seeker=seeker, action="moderation_ok", pk=pk)

    if request.is_ajax() and request.user.employer:
        add_delete_favorites(request)

    context = {'title': title, 'item': resume}

    return render(request, 'workerapp/resume_view.html', context)


@login_required
def search_vacancy(request, seeker_id):
    title = 'Поиск вакансий'
    worker = get_object_or_404(Seeker, pk=seeker_id)
    search_vac = request.GET.get('search_vacancy')
    company = request.GET.get('company')
    city_vacancy = request.GET.get('city_vacancy')
    vacancy_type = request.GET.get('type')
    salary_level = request.GET.get('salary_level')
    currency = request.GET.get('currency')
    published_from = request.GET.get('published_from')
    published_till = request.GET.get('published_till')
    results = None
    if search_vac:
        results = Vacancy.objects.filter(Q(vacancy_name__icontains=search_vac) | Q(description__icontains=search_vac), action='moderation_ok', hide=False).order_by('-published')

    if company:
        if results:
            results = results.filter(employer__company_name__icontains=company)
        else:
            results = Vacancy.objects.filter(employer__company_name__icontains=company, action='moderation_ok', hide=False).order_by('-published')

    if city_vacancy:
        if results:
            results = results.filter(city=city_vacancy)
        else:
            results = Vacancy.objects.filter(city=city_vacancy, action='moderation_ok', hide=False).order_by('-published')

    if vacancy_type != '------':
        if results:
            results = results.filter(vacancy_type=vacancy_type)
        else:
            results = Vacancy.objects.filter(vacancy_type=vacancy_type, action='moderation_ok', hide=False).order_by('-published')

    if salary_level:
        if results:
            results = results.filter(min_salary__lte=salary_level, currency=currency)
        else:
            results = Vacancy.objects.filter(min_salary__lte=salary_level, currency=currency, action='moderation_ok', hide=False).order_by('-published')

    if published_from:
        if results:
            results = results.filter(published__gte=published_from)
        else:
            results = Vacancy.objects.filter(published__gte=published_from, action='moderation_ok', hide=False).order_by('-published')

    if published_till:
        if results:
            results = results.filter(published__lte=published_till)
        else:
            results = Vacancy.objects.filter(published__lte=published_till, action='moderation_ok', hide=False).order_by('-published')

    page = request.GET.get('page')
    paginator = Paginator(results, 1)
    try:
        search_paginator = paginator.page(page)
    except PageNotAnInteger:
        search_paginator = paginator.page(1)
    except EmptyPage:
        search_paginator = paginator.page(paginator.num_pages)
    context = {'title': title, 'object_list': search_paginator, 'worker': worker}
    return render(request, 'workerapp/search_vacancy.html', context)


@login_required
def my_responses(request, seeker_id):
    title = 'Отклики по резюме'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resumes = Resume.objects.filter(seeker=seeker, action="moderation_ok", hide=False).order_by('published')
    responses = SendOffers.objects.filter(resume__in=resumes).select_related()
    resumes_all = Resume.objects.filter(Q(action='moderation_ok') | Q(action='moderation_reject'),
                                        seeker=seeker).exclude(action='draft').exclude(hide=True).order_by('published')
    drafts = Resume.objects.filter(action='draft', hide=False, seeker=seeker).order_by('published')
    resumes_hide = Resume.objects.filter(hide=True, seeker=seeker).order_by('published')
    send_resp = SendResponse.objects.filter(resume__seeker=seeker.id).order_by('date')
    favorite_vacancies = FavoriteVacancies.objects.filter(seeker=seeker).order_by('-date')

    context = {'title': title, 'responses': responses, 'seeker': seeker, 'drafts': drafts, 'resumes_hide': resumes_hide,
               'resumes': resumes, 'resumes_all': resumes_all, 'send_resp': send_resp, 'favorites': favorite_vacancies}

    return render(request, 'workerapp/seeker_responses.html', context)


@login_required
def send_response(request, seeker_id, pk):
    title = 'Отклик на вакансию'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    vacancy = get_object_or_404(Vacancy, pk=pk)
    sent = False

    if request.method == 'POST':
        form = SendResponseForm(request.POST, seeker=seeker)
        send = SendResponse()

        if form.is_valid():
            send.resume = form.cleaned_data.get('resume')
            send.cover_letter = form.cleaned_data.get('cover_letter')
            send.vacancy = vacancy
            send.save()
            sent = True

    else:
        form = SendResponseForm(seeker=seeker)

    context = {'title': title, 'form': form, 'sent': sent, 'seeker': seeker, 'vacancy': vacancy}

    return render(request, 'workerapp/send_response.html', context)


@login_required
def send_responses(request, seeker_id):
    title = 'Направленные отклики по вакансиям'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    send_resp = SendResponse.objects.filter(resume__seeker=seeker.id).order_by('date')
    resumes = Resume.objects.filter(action='moderation_ok', hide=False, seeker=seeker).order_by('published')
    resumes_all = Resume.objects.filter(Q(action='moderation_ok') | Q(action='moderation_reject'),
                                        seeker=seeker).exclude(action='draft').exclude(hide=True).order_by('published')
    drafts = Resume.objects.filter(action='draft', hide=False, seeker=seeker).order_by('published')
    resumes_hide = Resume.objects.filter(hide=True, seeker=seeker).order_by('published')
    responses = SendOffers.objects.filter(resume__in=resumes).select_related()
    favorite_vacancies = FavoriteVacancies.objects.filter(seeker=seeker).order_by('-date')

    context = {'title': title, 'seeker': seeker, 'send_resp': send_resp, 'resumes': resumes, 'resumes_all': resumes_all,
               'drafts': drafts, 'responses': responses, 'resumes_hide': resumes_hide, 'favorites': favorite_vacancies}

    return render(request, 'workerapp/seeker_send_responses.html', context)


@login_required
def seeker_profile(request, seeker_id):
    title = 'Профиль соискателя'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    resumes = Resume.objects.filter(action='moderation_ok', hide=False, seeker=seeker).order_by('published')

    context = {'title': title, 'seeker': seeker, 'resumes': resumes}

    return render(request, 'workerapp/seeker_profile.html', context)


@login_required
def delete_favorite(request, seeker_id, pk):
    title = 'Удаление избранных вакансий'
    seeker = get_object_or_404(Seeker, pk=seeker_id)
    favorite = get_object_or_404(FavoriteVacancies, pk=pk)

    if request.method == 'POST':
        favorite.delete()
        return HttpResponseRedirect(reverse('worker:favorites', args=[seeker.pk]))

    context = {'title': title, 'favorite': favorite, 'seeker': seeker}

    return render(request, 'workerapp/delete_favorite.html', context)


@login_required
def response_ajax(request):
    if request.user.employer and request.is_ajax():
        resume_id = request.GET.get('resume_id')
        resume = get_object_or_404(Resume, pk=resume_id)
        send_response = SendResponse.objects.get(resume=resume)
        status_id = request.GET.get('status_id')
        if status_id == 'новое (не прочитано)':
            send_response.status = SendResponse.READ
            send_response.save()
            return send_response