from django.urls import path

from workerapp import views

app_name = 'workerapp'

urlpatterns = [
    path('', views.worker_cabinet, name='main')
]
