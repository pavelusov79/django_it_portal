from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import EmployerRegisterForm, UserLoginForm, UserEditForm, EmployerEditForm, \
    SeekerRegisterForm, SeekerEditForm, UserSeekerEditForm
from authapp.models import Employer, Seeker


def register(request):
    title = 'регистрация работодателя'

    if request.method == 'POST':
        register_form = EmployerRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            employer = Employer.objects.create(user=user)
            employer.company_name = register_form.cleaned_data.get('company_name')
            employer.logo = register_form.cleaned_data.get('logo')
            employer.short_description = register_form.cleaned_data.get('short_description')
            employer.tel = register_form.cleaned_data.get('tel')
            employer.web = register_form.cleaned_data.get('web')

            employer.save()

            return HttpResponseRedirect(reverse('auth:login'))

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
            seeker = Seeker.objects.create(user=user)
            seeker.sex = register_form.cleaned_data.get('sex')
            seeker.hobby = register_form.cleaned_data.get('hobby')
            seeker.skills = register_form.cleaned_data.get('skills')
            seeker.tel = register_form.cleaned_data.get('tel')
            seeker.married = register_form.cleaned_data.get('married')
            seeker.photo = register_form.cleaned_data.get('photo')
            seeker.patronimyc = register_form.cleaned_data.get('patronimyc')
            seeker.age = register_form.cleaned_data.get('age')

            seeker.save()

            return HttpResponseRedirect(reverse('auth:login'))

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
            return HttpResponseRedirect(reverse('main'))

    content = {'title': title, 'login_form': login_form }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


@login_required
def edit(request):
    title = 'редактирование работодателя'
    sent = False
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, instance=request.user)
        employer_form = EmployerEditForm(request.POST, request.FILES,
                                         instance=request.user.employer)
        if edit_form.is_valid() and employer_form.is_valid():
            edit_form.save()
            employer_form.save()
            # return HttpResponseRedirect(reverse('main'))
            sent = True
    else:
        edit_form = UserEditForm(instance=request.user)
        employer_form = EmployerEditForm(instance=request.user.employer)

    content = {'title': title, 'edit_form': edit_form, 'employer_form': employer_form, 'sent': sent}

    return render(request, 'authapp/edit.html', content)


@login_required
def edit_seeker(request):
    title = 'редактирование соискателя'
    sent = False
    if request.method == 'POST':
        edit_form = UserSeekerEditForm(request.POST, instance=request.user)
        seeker_form = SeekerEditForm(request.POST, request.FILES, instance=request.user.seeker)
        if edit_form.is_valid() and seeker_form.is_valid():
            edit_form.save()
            seeker_form.save()
            # return HttpResponseRedirect(reverse('main'))
            sent = True
    else:
        edit_form = UserSeekerEditForm(instance=request.user)
        seeker_form = SeekerEditForm(instance=request.user.seeker)

    content = {'title': title, 'edit_form': edit_form, 'seeker_form': seeker_form, 'sent': sent}

    return render(request, 'authapp/edit_seeker.html', content)
