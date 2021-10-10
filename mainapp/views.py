from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from authapp.views import UserLoginView
from authapp.models import Employer
from employerapp.models import Vacancy, FavoriteResumes
from mainapp.models import News
from workerapp.models import Resume, FavoriteVacancies


class MainView(UserLoginView, ListView):
    template_name = 'mainapp/index.html'
    paginate_by = 2

    def get_queryset(self):
        try:
            if self.request.user.employer:
                return Resume.objects.filter(action='moderation_ok', hide=False).order_by('-published')
        except Employer.DoesNotExist:
            pass
        except AttributeError:
            return []
        try:
            if self.request.user.seeker:
                return Vacancy.objects.filter(action='moderation_ok', hide=False).order_by('-published')
        except AttributeError:
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['favorite_resumes'] = []
        context['favorite_vacancies'] = []
        try:
            favorite_resumes = FavoriteResumes.objects.filter(employer=self.request.user.employer)
            for item in favorite_resumes:
                context['favorite_resumes'].append(item.resume.position)
        except AttributeError:
            pass
        try:
            fav_vac = FavoriteVacancies.objects.filter(seeker=self.request.user.seeker)
            for item in fav_vac:
                context['favorite_vacancies'].append(item.vacancy.vacancy_name)
        except AttributeError:
            pass
        context['news'] = News.objects.filter(is_active=True).order_by('-published')[:3]
        context['employers'] = Employer.objects.filter(status='moderation_ok').order_by('?')[:6]
        return context


class NewsListView(ListView):
    queryset = News.objects.filter(is_active=True).order_by('-published')
    paginate_by = 4


class NewsDetailView(DetailView):
    model = News
    context_object_name = 'one_news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['pk']
        context['url'] = f'http://127.0.0.1:8000{self.request.path}'
        return context


class SearchNewsListView(ListView):
    template_name = 'mainapp/search_news.html'
    paginate_by = 4

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            results = News.objects.filter(Q(title__icontains=search) | Q(description__icontains=search),
                                          is_active=True).order_by('-published')
            return results
        return News.objects.all().order_by('-published')


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
