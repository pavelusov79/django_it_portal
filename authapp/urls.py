from django.urls import path, re_path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('register/', authapp.register, name='register'),
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('edit/', authapp.edit, name='edit'),
    path('register_seeker/', authapp.register_seeker, name='register_seeker'),
    path('edit_seeker/', authapp.edit_seeker, name='edit_seeker'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify'),
    re_path(r'^seeker_verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.seeker_verify, name='seeker_verify'),
    path('email_verify/', authapp.email_verify, name='email_verify'),
    path('edit_password/', authapp.change_password, name='change_password')
]
