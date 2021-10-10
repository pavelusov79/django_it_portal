from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, DeleteView, UpdateView, ListView, CreateView
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from authapp.models import Employer
from employerapp.forms import VacancyCreationForm, SendOfferForm
from employerapp.models import Vacancy, SendOffers, FavoriteResumes
from mainapp.views import change_favorites_vacancies
from workerapp.models import Resume, SendResponse, FavoriteVacancies


class DataMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employer'] = get_object_or_404(Employer, pk=kwargs['emp_id'])
        context['vacancies'] = Vacancy.objects.filter(action='moderation_ok', hide=False,
                                                      employer=context['employer']).order_by('published')
        context['drafts'] = Vacancy.objects.filter(action='draft', hide=False,
                                                   employer=context['employer']).order_by('published')
        context['vacancies_hide'] = Vacancy.objects.filter(hide=True,
                                                           employer=context['employer']).order_by('published')
        context['vacancies_all'] = Vacancy.objects.filter(Q(action='moderation_ok') | Q(action='moderation_reject'),
                                                          employer=context['employer']).exclude(action='draft',
                                                          hide=True).order_by('published')
        context['offers'] = SendOffers.objects.filter(vacancy__employer=context['employer'].pk).order_by('date')
        context['take_offers'] = SendResponse.objects.filter(vacancy__in=context['vacancies']).select_related()
        context['favorites'] = FavoriteResumes.objects.filter(employer=context['employer']).order_by('date')
        return context


class EmployerCabinetView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'employerapp/employer_cabinet.html'
    extra_context = {'title': 'Личный кабинет работодателя'}


class VacancyPublishedView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'employerapp/vacancy_published.html'
    extra_context = {'title': 'Опубликованные вакансии'}


class VacancyDraftView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'employerapp/vacancy_drafts.html'
    extra_context = {'title': 'Черновики'}


class MessagesView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'employerapp/employer_messages.html'
    extra_context = {'title': 'Сообщения от админа портала'}


class VacancyHideView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'employerapp/vacancy_hide.html'
    extra_context = {'title': 'Удаленные вакансии'}


class SendOffersView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'employerapp/employer_offers.html'
    extra_context = {'title': 'Направленные предложения'}


class MyOffersView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'employerapp/offers_list.html'
    extra_context = {'title': 'Отклики по вакансиям'}


class FavoritesResumeView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'employerapp/favorites.html'
    extra_context = {'title': 'Избранные резюме'}


class CompanyProfileView(TemplateView):
    template_name = 'employerapp/company_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employer'] = get_object_or_404(Employer, pk=kwargs['emp_id'])
        context['vacancies'] = Vacancy.objects.filter(action='moderation_ok', hide=False,
                                                      employer=context['employer']).order_by('published')
        context['title'] = 'Профиль компании'
        return context


class VacancyDetailView(LoginRequiredMixin, DetailView):
    model = Vacancy
    context_object_name = 'item'
    template_name = 'employerapp/vacancy_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employer'] = get_object_or_404(Employer, pk=self.kwargs['emp_id'])
        context['favorite'] = FavoriteVacancies.objects.filter(vacancy=self.object,
                                                               seeker=self.request.user.seeker).first()
        context['title'] = 'Вакансия'
        if self.request.is_ajax() and self.request.user.seeker:
            change_favorites_vacancies(self.request)
        return context


class CreateVacancyView(LoginRequiredMixin, CreateView):
    model = Vacancy
    template_name = 'employerapp/vacancy_creation.html'
    form_class = VacancyCreationForm
    success_url = 'vacancy_creation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'создание вакансии'
        context['employer'] = get_object_or_404(Employer, pk=self.kwargs['emp_id'])
        context['sent'] = False
        context['action'] = None
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.action = form.cleaned_data.get('action')
            obj.employer = context['employer']
            obj.save()
            context['sent'] = True
            context['action'] = obj.action
            super().form_valid(form)
        return render(self.request, self.template_name, context)


class VacancyEditView(LoginRequiredMixin, UpdateView):
    template_name = 'employerapp/vacancy_creation.html'
    model = Vacancy
    form_class = VacancyCreationForm
    success_url = 'vacancy_edit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование вакансии'
        context['employer'] = get_object_or_404(Employer, pk=self.kwargs['emp_id'])
        context['sent'] = False
        context['action'] = None
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.fall_moderation = ''
            obj.action = form.cleaned_data.get('action')
            obj.save()
            context['sent'] = True
            context['action'] = obj.action
            super().form_valid(form)
        return render(self.request, self.template_name, context)


class VacancyDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacancy
    context_object_name = 'vacancy_delete'
    template_name = 'employerapp/vacancy_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employer'] = get_object_or_404(Employer, pk=self.kwargs['emp_id'])
        context['title'] = 'Удаление вакансии'
        return context

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.action == 'draft' or obj.action == 'moderation_ok':
            if not obj.hide:
                obj.hide = True
            else:
                obj.hide = False
            obj.save()
            return HttpResponseRedirect(reverse('employer:cabinet', args=[obj.employer.pk]))


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


class SendOfferCreateView(LoginRequiredMixin, CreateView):
    template_name = 'employerapp/send_offer.html'
    form_class = SendOfferForm
    success_url = 'send_offer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Предложение по работе'
        context['sent'] = False
        context['employer'] = get_object_or_404(Employer, pk=self.kwargs['emp_id'])
        context['resume'] = get_object_or_404(Resume, pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employer'] = get_object_or_404(Employer, pk=self.kwargs['emp_id'])
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        send = SendOffers()
        if form.is_valid():
            send.vacancy = form.cleaned_data.get('vacancy')
            send.cover_letter = form.cleaned_data.get('cover_letter')
            send.contact_phone = form.cleaned_data.get('contact_phone')
            send.resume = context['resume']
            send.save()
            context['sent'] = True
            return render(self.request, self.template_name, context)


class DeleteFavoriteResumeView(LoginRequiredMixin, DeleteView):
    model = FavoriteResumes
    template_name = 'employerapp/delete_favorite.html'
    context_object_name = 'favorite'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление избранных резюме'
        context['employer'] = get_object_or_404(Employer, pk=self.kwargs['emp_id'])
        return context

    def get_success_url(self):
        context = self.get_context_data()
        employer = context['employer']
        return reverse('employer:favorites', args=[employer.pk])


class SearchResumeListView(LoginRequiredMixin, ListView):
    paginate_by = 1
    template_name = 'employerapp/search_resume.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Поиск резюме'
        context['employer'] = get_object_or_404(Employer, pk=self.kwargs['emp_id'])
        context['fav_list'] = []
        favorite_resumes = FavoriteResumes.objects.filter(employer=context['employer'])
        for item in favorite_resumes:
            context['fav_list'].append(item.resume.position)
        return context

    def get_queryset(self):
        search = self.request.GET.get('search')
        city = self.request.GET.get('city')
        salary = self.request.GET.get('salary')
        currency = self.request.GET.get('currency')
        gender = self.request.GET.get('gender')
        from_date = self.request.GET.get('from_date')
        till_date = self.request.GET.get('till_date')
        results = []
        if search:
            results = Resume.objects.filter(Q(position__icontains=search) |
                                            Q(skills__icontains=search)).filter(action='moderation_ok',
                                                                                hide=False).order_by('-published')

        if city:
            if results:
                results = results.filter(seeker__city=city)
            else:
                results = Resume.objects.filter(seeker__city=city, action='moderation_ok',
                                                hide=False).order_by('-published')

        if gender == 'female' or gender == 'male':
            if results:
                results = results.filter(seeker__sex=gender)
            else:
                results = Resume.objects.filter(seeker__sex=gender, action='moderation_ok',
                                                hide=False).order_by('-published')

        if salary:
            if results:
                results = results.filter(min_salary__lte=salary, currency=currency)
            else:
                results = Resume.objects.filter(min_salary__lte=salary, currency=currency,
                                                action='moderation_ok', hide=False).order_by('-published')

        if from_date:
            if results:
                results = results.filter(published__gte=from_date)
            else:
                results = Resume.objects.filter(published__gte=from_date, action='moderation_ok',
                                                hide=False).order_by('-published')

        if till_date:
            if results:
                results = results.filter(published__lte=till_date)
            else:
                results = Resume.objects.filter(published__lte=till_date, action='moderation_ok',
                                                hide=False).order_by('-published')
        return results
