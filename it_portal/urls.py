"""it_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.MainView.as_view(), name='main'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('search_news/', views.SearchNewsListView.as_view(), name='search_news'),
    path('news/detail/<int:pk>/', views.NewsDetailView.as_view(), name="news_detail"),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('employer/', include('employerapp.urls', namespace='employer')),
    path('worker/', include('workerapp.urls', namespace='worker')),
    path('favorites_ajax/', views.add_delete_favorites, name="favorites_ajax"),
    path('favorite_vacancies_ajax/', views.change_favorites_vacancies, name="favorites_vacancies_ajax")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)