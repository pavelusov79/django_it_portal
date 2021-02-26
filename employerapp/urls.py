from django.urls import path

from employerapp import views

app_name = 'employerapp'

urlpatterns = [
    path('', views.employer_cabinet, name='main')
]
