from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DeleteView, DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from authapp.models import Seeker
from employerapp.models import Vacancy, SendOffers, FavoriteResumes
from mainapp.views import add_delete_favorites
from workerapp.forms import ResumeEducationForm, ResumeExperienceForm, ResumeForm, SendResponseForm
from workerapp.models import ResumeExperience, ResumeEducation, Resume, SendResponse, FavoriteVacancies


class DataMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seeker'] = get_object_or_404(Seeker, pk=kwargs['seeker_id'])
        context['resumes_all'] = Resume.objects.filter(Q(action='moderation_ok') | Q(action='moderation_reject'),
                                                       seeker=context['seeker']).exclude(action='draft',
                                                                                         hide=True).order_by('published')
        context['resumes'] = Resume.objects.filter(action='moderation_ok', hide=False,
                                                   seeker=context['seeker']).order_by('published')
        context['drafts'] = Resume.objects.filter(action='draft', hide=False,
                                                  seeker=context['seeker']).order_by('published')
        context['resumes_hide'] = Resume.objects.filter(hide=True, seeker=context['seeker']).order_by('published')
        context['responses'] = SendOffers.objects.filter(resume__in=context['resumes']).select_related()
        context['send_resp'] = SendResponse.objects.filter(resume__seeker=context['seeker'].id).order_by('date')
        context['favorites'] = FavoriteVacancies.objects.filter(seeker=context['seeker']).order_by('-date')
        return context


class WorkerCabinetView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'workerapp/worker_cabinet.html'
    extra_context = {'title': 'Личный кабинет соискателя'}


class MessagesView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'workerapp/worker_messages.html'
    extra_context = {'title': 'Сообщения от админа портала'}


class HideResumesView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'workerapp/resume_hide.html'
    extra_context = {'title': 'Удаленные/скрытые резюме'}


class ResumeDraftsView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'workerapp/resume_drafts.html'
    extra_context = {'title': 'Черновики резюме'}


class PublishedResumesView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'workerapp/resume_published.html'
    extra_context = {'title': 'Опубликованные резюме'}


class FavoriteVacanciesView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'workerapp/favorites.html'
    extra_context = {'title': 'Избранные вакансии'}


class MyResponsesView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'workerapp/seeker_responses.html'
    extra_context = {'title': 'Отклики по резюме'}


class SendResponsesView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'workerapp/seeker_send_responses.html'
    extra_context = {'title': 'Направленные отклики по вакансиям'}


class SeekerProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'workerapp/seeker_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль соискателя'
        context['seeker'] = get_object_or_404(Seeker, pk=self.kwargs['seeker_id'])
        context['resumes'] = Resume.objects.filter(action='moderation_ok', hide=False,
                                                   seeker=context['seeker']).order_by('published')
        return context


class ResumeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'workerapp/resume_creation.html'
    form_class = ResumeForm
    success_url = 'resume_creation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание резюме'
        context['seeker'] = get_object_or_404(Seeker, pk=self.kwargs['seeker_id'])
        context['sent'] = False
        context['status'] = None
        self.education_formset = inlineformset_factory(Resume, ResumeEducation, form=ResumeEducationForm, extra=1)
        self.experience_formset = inlineformset_factory(Resume, ResumeExperience, form=ResumeExperienceForm, extra=1)
        context['education_form'] = self.education_formset(prefix='1')
        context['experience_form'] = self.experience_formset(prefix='2')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        if form.is_valid():
            resume = form.save(commit=False)
            resume.seeker = context['seeker']
            resume.action = form.cleaned_data.get('action')
            resume.save()
            context['education_form'] = self.education_formset(self.request.POST, prefix='1', instance=resume)
            context['experience_form'] = self.experience_formset(self.request.POST, prefix='2', instance=resume)
            if context['education_form'].is_valid():
                context['education_form'].save()
            if context['experience_form'].is_valid():
                context['experience_form'].save()
            context['sent'] = True
            context['status'] = resume.action
            super().form_valid(form)
        return render(self.request, self.template_name, context)


class ResumeUpdateView(LoginRequiredMixin, UpdateView):
    model = Resume
    template_name = 'workerapp/resume_creation.html'
    form_class = ResumeForm
    context_object_name = 'resume'
    success_url = 'resume_update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование резюме'
        context['seeker'] = get_object_or_404(Seeker, pk=self.kwargs['seeker_id'])
        context['sent'] = False
        context['status'] = None
        education_formset = inlineformset_factory(Resume, ResumeEducation, form=ResumeEducationForm, extra=1)
        experience_formset = inlineformset_factory(Resume, ResumeExperience, form=ResumeExperienceForm, extra=1)
        if self.request.POST:
            context['education_form'] = education_formset(self.request.POST, prefix='1', instance=self.object)
            context['experience_form'] = experience_formset(self.request.POST, prefix='2', instance=self.object)
        else:
            context['education_form'] = education_formset(prefix='1', instance=self.object)
            context['experience_form'] = experience_formset(prefix='2', instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        if form.is_valid() and context['education_form'].is_valid() and context['experience_form'].is_valid():
            obj = form.save(commit=False)
            obj.failed_moderation = ''
            obj.action = form.cleaned_data.get('action')
            obj.failed_moderation = ''
            obj.save()
            context['education_form'].save()
            context['experience_form'].save()
            context['sent'] = True
            context['status'] = obj.action
            print('status= ', context['status'])
            super().form_valid(form)
        return render(self.request, self.template_name, context)


class DeleteResumeView(LoginRequiredMixin, DeleteView):
    model = Resume
    template_name = 'workerapp/resume_delete.html'
    context_object_name = 'resume_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление резюме'
        context['seeker'] = get_object_or_404(Seeker, pk=self.kwargs['seeker_id'])
        return context

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.action == 'draft' or obj.action == 'moderation_ok':
            if not obj.hide:
                obj.hide = True
            else:
                obj.hide = False
            obj.save()
            return HttpResponseRedirect(reverse('worker:seeker_cabinet', args=[obj.seeker.pk]))


class FavoriteVacancyDeleteView(LoginRequiredMixin, DeleteView):
    model = FavoriteVacancies
    template_name = 'workerapp/delete_favorite.html'
    context_object_name = 'favorite'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление избранных вакансий'
        context['seeker'] = get_object_or_404(Seeker, pk=self.kwargs['seeker_id'])
        return context

    def get_success_url(self):
        context = self.get_context_data()
        seeker = context['seeker']
        return reverse('worker:favorites', args=[seeker.pk])


class ResumeExperienceDeleteView(LoginRequiredMixin, DeleteView):
    model = ResumeExperience
    template_name = 'workerapp/resume_experience_delete.html'
    context_object_name = 'experience'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление записи об опыте из резюме'
        context['seeker'] = get_object_or_404(Seeker, pk=self.kwargs['seeker_id'])
        context['resume'] = get_object_or_404(Resume, pk=self.kwargs['resume_id'])
        return context

    def get_success_url(self):
        context = self.get_context_data()
        seeker = context['seeker']
        resume = context['resume']
        if resume.action == 'draft':
            return reverse('worker:drafts', args=[seeker.pk])
        else:
            return reverse('worker:published', args=[seeker.pk])


class ResumeEducationDeleteView(LoginRequiredMixin, DeleteView):
    model = ResumeEducation
    template_name = 'workerapp/resume_education_delete.html'
    context_object_name = 'education'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление записи об образовании из резюме'
        context['seeker'] = get_object_or_404(Seeker, pk=self.kwargs['seeker_id'])
        context['resume'] = get_object_or_404(Resume, pk=self.kwargs['resume_id'])
        return context

    def get_success_url(self):
        context = self.get_context_data()
        seeker = context['seeker']
        resume = context['resume']
        if resume.action == 'draft':
            return reverse('worker:drafts', args=[seeker.pk])
        else:
            return reverse('worker:published', args=[seeker.pk])


class ResumeDetailView(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = 'workerapp/resume_view.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Резюме"
        context['seeker'] = get_object_or_404(Seeker, pk=self.kwargs['seeker_id'])
        context['favorite'] = FavoriteResumes.objects.filter(resume=self.object,
                                                             employer=self.request.user.employer).first()
        if self.request.is_ajax() and self.request.user.employer:
            add_delete_favorites(self.request)
        return context


class SearchVacancyListView(LoginRequiredMixin, ListView):
    template_name = 'workerapp/search_vacancy.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Поиск вакансий'
        context['worker'] = get_object_or_404(Seeker, pk=self.kwargs['seeker_id'])
        context['fav_vacancies'] = []
        favorite_vacancies = FavoriteVacancies.objects.filter(seeker=context['worker'])
        for item in favorite_vacancies:
            context['fav_vacancies'].append(item.vacancy.vacancy_name)
        return context

    def get_queryset(self):
        search_vac = self.request.GET.get('search_vacancy')
        company = self.request.GET.get('company')
        city_vacancy = self.request.GET.get('city_vacancy')
        vacancy_type = self.request.GET.get('type')
        salary_level = self.request.GET.get('salary_level')
        currency = self.request.GET.get('currency')
        published_from = self.request.GET.get('published_from')
        published_till = self.request.GET.get('published_till')
        results = []
        if search_vac:
            results = Vacancy.objects.filter(
                Q(vacancy_name__icontains=search_vac) | Q(description__icontains=search_vac), action='moderation_ok',
                hide=False).order_by('-published')

        if company:
            if results:
                results = results.filter(employer__company_name__icontains=company)
            else:
                results = Vacancy.objects.filter(employer__company_name__icontains=company, action='moderation_ok',
                                                 hide=False).order_by('-published')

        if city_vacancy:
            if results:
                results = results.filter(city=city_vacancy)
            else:
                results = Vacancy.objects.filter(city=city_vacancy, action='moderation_ok', hide=False).order_by(
                    '-published')

        if vacancy_type != '------':
            if results:
                results = results.filter(vacancy_type=vacancy_type)
            else:
                results = Vacancy.objects.filter(vacancy_type=vacancy_type, action='moderation_ok',
                                                 hide=False).order_by('-published')

        if salary_level:
            if results:
                results = results.filter(min_salary__lte=salary_level, currency=currency)
            else:
                results = Vacancy.objects.filter(min_salary__lte=salary_level, currency=currency,
                                                 action='moderation_ok', hide=False).order_by('-published')

        if published_from:
            if results:
                results = results.filter(published__gte=published_from)
            else:
                results = Vacancy.objects.filter(published__gte=published_from, action='moderation_ok',
                                                 hide=False).order_by('-published')

        if published_till:
            if results:
                results = results.filter(published__lte=published_till)
            else:
                results = Vacancy.objects.filter(published__lte=published_till, action='moderation_ok',
                                                 hide=False).order_by('-published')
        return results


class SendResponseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'workerapp/send_response.html'
    form_class = SendResponseForm
    success_url = 'send_response'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отклик на вакансию'
        context['seeker'] = get_object_or_404(Seeker, pk=self.kwargs['seeker_id'])
        context['vacancy'] = get_object_or_404(Vacancy, pk=self.kwargs['pk'])
        context['sent'] = False
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['seeker'] = get_object_or_404(Seeker, pk=self.kwargs['seeker_id'])
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        send = SendResponse()
        if form.is_valid():
            send.resume = form.cleaned_data.get('resume')
            send.cover_letter = form.cleaned_data.get('cover_letter')
            send.vacancy = context['vacancy']
            send.save()
            context['sent'] = True
            return render(self.request, self.template_name, context)


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