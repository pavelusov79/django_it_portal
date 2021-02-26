from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('register/', authapp.register, name='register'),
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('edit/', authapp.edit, name='edit'),
    path('register_seeker/', authapp.register_seeker, name='register_seeker'),
    path('edit_seeker/', authapp.edit_seeker, name='edit_seeker')
]
