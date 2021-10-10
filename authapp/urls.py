from django.urls import path, re_path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('register/', authapp.EmployerRegistrationView.as_view(), name='register'),
    path('login/', authapp.UserLoginView.as_view(), name='login'),
    path('logout/', authapp.LogoutUserView.as_view(), name='logout'),
    path('edit/<int:pk>/', authapp.EmployerUpdateView.as_view(), name='edit'),
    path('register_seeker/', authapp.SeekerRegistrationView.as_view(), name='register_seeker'),
    path('edit_seeker/<int:pk>/', authapp.SeekerUpdateView.as_view(), name='edit_seeker'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify'),
    re_path(r'^seeker_verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.seeker_verify, name='seeker_verify'),
    path('email_verify/', authapp.EmailVerifyView.as_view(), name='email_verify'),
    path('edit_password/', authapp.ChangePasswordView.as_view(), name='change_password')
]
