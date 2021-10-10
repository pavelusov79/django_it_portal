import hashlib
import random

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView, auth_login
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, UpdateView

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


class EmailVerifyView(TemplateView):
    template_name = 'authapp/email_verify.html'
    extra_context = {'title': 'подтверждение почты'}


class EmployerRegistrationView(CreateView):
    template_name = 'authapp/register.html'
    form_class = EmployerRegisterForm

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            employer = Employer.objects.create(user=user)
            employer.company_name = form.cleaned_data.get('company_name')
            employer.logo = form.cleaned_data.get('logo')
            employer.city = form.cleaned_data.get('city')
            employer.short_description = form.cleaned_data.get('short_description')
            employer.tel = form.cleaned_data.get('tel')
            employer.web = form.cleaned_data.get('web')
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
            employer.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
            employer.save()
            if send_verify_mail(user):
                return HttpResponseRedirect(reverse('auth:email_verify'))
            else:
                return HttpResponse('ошибка отправки сообщения о регистрации')


class SeekerRegistrationView(CreateView):
    template_name = 'authapp/register_seeker.html'
    form_class = SeekerRegisterForm

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            seeker = Seeker.objects.create(user=user)
            seeker.sex = form.cleaned_data.get('sex')
            seeker.tel = form.cleaned_data.get('tel')
            seeker.city = form.cleaned_data.get('city')
            seeker.married = form.cleaned_data.get('married')
            seeker.photo = form.cleaned_data.get('photo')
            seeker.patronimyc = form.cleaned_data.get('patronimyc')
            seeker.age = form.cleaned_data.get('age')
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
            seeker.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
            seeker.save()
            if send_verify_mail_seeker(user):
                return HttpResponseRedirect(reverse('auth:email_verify'))
            else:
                return HttpResponse('ошибка отправки сообщения о регистрации')


class UserLoginView(LoginView):
    template_name = 'authapp/login.html'
    authentication_form = UserLoginForm
    extra_context = {'title': 'вход'}

    def get_success_url(self):
        return reverse('main')

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if form.get_user().is_superuser:
            return HttpResponseRedirect(reverse('admin:index'))
        return HttpResponseRedirect(self.get_success_url())


class LogoutUserView(LogoutView):
    next_page = 'main'


class EmployerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'authapp/edit.html'
    model = Employer
    form_class = EmployerEditForm
    success_url = 'edit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'редактирование работодателя'
        context['sent'] = False
        if self.request.POST:
            context['edit_form'] = UserEditForm(self.request.POST,
                                                instance=User.objects.get(pk=self.request.user.pk))
        else:
            context['edit_form'] = UserEditForm(instance=User.objects.get(pk=self.request.user.pk))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        if form.is_valid() and context['edit_form'].is_valid():
            form.save()
            context['edit_form'].save()
            self.object.status = Employer.NEED_MODER
            self.object.failed_moderation = ''
            self.object.save()
            context['sent'] = True
            super().form_valid(form)
            return render(self.request, self.template_name, context)


class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'authapp/change_password.html'
    success_url = 'change_password'

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Смена пароля'
        context['sent'] = False
        context['form'] = SetPasswordForm()
        context['user'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        form = SetPasswordForm(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        context = self.get_context_data()
        if form.is_valid():
            obj = self.get_object()
            obj.set_password(form.cleaned_data['password1'])
            obj.save()
            update_session_auth_hash(self.request, obj)
            context['sent'] = True
            return render(self.request, self.template_name, context)


class SeekerUpdateView(LoginRequiredMixin, UpdateView):
    model = Seeker
    form_class = SeekerEditForm
    template_name = 'authapp/edit_seeker.html'
    success_url = 'edit_seeker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'редактирование соискателя'
        context['sent'] = False
        if self.request.POST:
            context['seeker_form'] = UserSeekerEditForm(self.request.POST,
                                                        instance=User.objects.get(pk=self.request.user.id))
        else:
            context['seeker_form'] = UserSeekerEditForm(instance=User.objects.get(pk=self.request.user.id))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        if form.is_valid and context['seeker_form'].is_valid():
            form.save()
            context['seeker_form'].save()
            context['sent'] = True
            self.object.status = Seeker.NEED_MODER
            self.object.failed_moderation = ''
            self.object.save()
            super().form_valid(form)
            return render(self.request, self.template_name, context)
