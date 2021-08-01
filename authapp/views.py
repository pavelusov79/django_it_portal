import hashlib
import random

from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from authapp.forms import EmployerRegisterForm, UserLoginForm, UserEditForm, EmployerEditForm, \
    SeekerRegisterForm, SeekerEditForm, UserSeekerEditForm, SetPasswordForm
from authapp.models import Employer, Seeker
from it_portal import settings


def send_verify_mail(user):
    if user.employer:
        verify_link = reverse('auth:verify', args=[user.email, user.employer.activation_key])
        title = f'Подтверждение почты {user.email}'
        message = f'Сообщение с сайта IT Recrut\nПросим вас в течении 24-х часов  с момента получения ' \
                  f'данного письма подтвердить адрес своей электронной почты\nПросим пройти по ссылке {settings.DOMAIN_NAME}{verify_link}'

        return send_mail(title, message, 'it.portal.gb@gmail.com', [user.email], fail_silently=False)
    else:
        print('user has no object employer')


def send_verify_mail_seeker(user):
    if user.seeker:
        verify_link = reverse('auth:seeker_verify', args=[user.email, user.seeker.activation_key])
        title = f'Подтверждение почты {user.email}'
        message = f'Сообщение с сайта IT Recrut\nПросим вас в течении 24-х часов  с момента получения ' \
                  f'данного письма подтвердить адрес своей электронной почты\nПросим пройти по ссылке {settings.DOMAIN_NAME}{verify_link}'

        return send_mail(title, message, 'it.portal.gb@gmail.com', [user.email], fail_silently=False)
    else:
        print('user has no object seeker')


def verify(request, email, activation_key):
    title = 'Подтверждение регистрации'
    user = User.objects.get(email=email)
    if user.employer.activation_key == activation_key and not \
            user.employer.is_activation_key_expired():
        user.is_active = True
        user.save()
        return render(request, 'authapp/verification.html', {'user': user, 'title': title})


def seeker_verify(request, email, activation_key):
    title = 'Подтверждение регистрации'
    user = User.objects.get(email=email)
    if user.seeker.activation_key == activation_key and not \
            user.seeker.is_activation_key_expired():
        user.is_active = True
        user.save()
        return render(request, 'authapp/verification.html', {'user': user, 'title': title})


def email_verify(request):
    title = 'подтверждение почты'
    context = {'title': title}
    return render(request, 'authapp/email_verify.html', context)


def register(request):
    title = 'регистрация работодателя'

    if request.method == 'POST':
        register_form = EmployerRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            user.is_active = False
            user.save()
            employer = Employer.objects.create(user=user)
            employer.company_name = register_form.cleaned_data.get('company_name')
            employer.logo = register_form.cleaned_data.get('logo')
            employer.city = register_form.cleaned_data.get('city')
            employer.short_description = register_form.cleaned_data.get('short_description')
            employer.tel = register_form.cleaned_data.get('tel')
            employer.web = register_form.cleaned_data.get('web')
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
            employer.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
            employer.save()
            if send_verify_mail(user):
                return HttpResponseRedirect(reverse('auth:email_verify'))
            else:
                return HttpResponse('ошибка отправки сообщения о регистрации')

    else:
        register_form = EmployerRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


def register_seeker(request):
    title = 'регистрация соискателя'

    if request.method == 'POST':
        register_form = SeekerRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            user.is_active = False
            user.save()
            seeker = Seeker.objects.create(user=user)
            seeker.sex = register_form.cleaned_data.get('sex')
            seeker.tel = register_form.cleaned_data.get('tel')
            seeker.city = register_form.cleaned_data.get('city')
            seeker.married = register_form.cleaned_data.get('married')
            seeker.photo = register_form.cleaned_data.get('photo')
            seeker.patronimyc = register_form.cleaned_data.get('patronimyc')
            seeker.age = register_form.cleaned_data.get('age')
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
            seeker.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
            seeker.save()
            if send_verify_mail_seeker(user):
                return HttpResponseRedirect(reverse('auth:email_verify'))

            else:
                return HttpResponse('ошибка отправки сообщения о регистрации')

    else:
        register_form = SeekerRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register_seeker.html', content)


def login(request):

    title = 'вход'

    login_form = UserLoginForm(data=request.POST or None)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect(reverse('admin:index'))
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {'title': title, 'login_form': login_form}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


@login_required
def edit(request):
    title = 'редактирование работодателя'
    sent = False
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, instance=request.user)
        employer_form = EmployerEditForm(request.POST, request.FILES,
                                         instance=request.user.employer)
        if edit_form.is_valid() and employer_form.is_valid():
            edit_form.save()
            employer_form.save()
            user.employer.status = user.employer.NEED_MODER
            user.employer.failed_moderation = ''
            user.employer.save()
            sent = True
    else:
        edit_form = UserEditForm(instance=request.user)
        employer_form = EmployerEditForm(instance=request.user.employer)

    content = {'title': title, 'edit_form': edit_form, 'employer_form': employer_form,
               'sent': sent}

    return render(request, 'authapp/edit.html', content)


@login_required
def change_password(request):
    title = 'Смена пароля'
    sent = False
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        password_form = SetPasswordForm(request.POST)
        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)
            sent = True
    else:
        password_form = SetPasswordForm()
    context = {'title': title, 'form': password_form, 'user': user, 'sent': sent}
    return render(request, 'authapp/change_password.html', context)


@login_required
def edit_seeker(request):
    title = 'редактирование соискателя'
    sent = False
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        edit_form = UserSeekerEditForm(request.POST, instance=request.user)
        seeker_form = SeekerEditForm(request.POST, request.FILES, instance=request.user.seeker)
        if edit_form.is_valid() and seeker_form.is_valid():
            edit_form.save()
            seeker_form.save()
            user.seeker.status = user.seeker.NEED_MODER
            user.seeker.failed_moderation = ''
            user.seeker.save()
            sent = True
    else:
        edit_form = UserSeekerEditForm(instance=request.user)
        seeker_form = SeekerEditForm(instance=request.user.seeker)

    content = {'title': title, 'edit_form': edit_form, 'seeker_form': seeker_form, 'sent': sent}

    return render(request, 'authapp/edit_seeker.html', content)
