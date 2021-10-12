from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from authapp.models import Employer, Seeker


class EmployerRegisterForm(UserCreationForm):
    company_name = forms.CharField()
    tel = forms.IntegerField()
    city = forms.CharField()
    web = forms.CharField()
    short_description = forms.CharField()
    logo = forms.ImageField(required=False)

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'company_name', 'email', 'city', 'web', 'tel', 'short_description',
                  'logo', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(EmployerRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label='Ваш логин на портале')
        self.fields['password1'] = forms.CharField(label='Пароль', widget=forms.PasswordInput)
        self.fields['password2'] = forms.CharField(label='Подтвердите пароль',
                                                   widget=forms.PasswordInput)
        self.fields['email'] = forms.EmailField(label='Ваш email')
        self.fields['city'] = forms.CharField(label='Ваш город')
        self.fields['tel'] = forms.CharField(label='Телефон компании', validators=[
                    RegexValidator(regex='^8[0-9]{10}$', message='Допускаются только цифры '
                    'начиная с 8-ки, например 84952354422 или 89147900000.')])
        self.fields['web'] = forms.CharField(label='Вебсайт компании', help_text='Поле необязательно', required=False)
        self.fields['short_description'] = forms.CharField(label='Краткое описание вашей '
                                            'компании', widget=forms.Textarea(attrs={'rows': 5}))
        self.fields['logo'] = forms.ImageField(label='Ваш логотип', required=False,
                                               help_text='Поле необязательно')
        self.fields['company_name'] = forms.CharField(label='Название вашей компании')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        data = self.cleaned_data['email']
        email_db = User.objects.filter(email=data).first()
        if email_db:
            raise forms.ValidationError('Пользователь с такой электронной почтой уже зарегистрирован')
        return data


class SeekerRegisterForm(UserCreationForm):
    patronimyc = forms.CharField()
    tel = forms.CharField()
    city = forms.CharField()
    sex = forms.ChoiceField()
    married = forms.ChoiceField()
    photo = forms.ImageField()
    age = forms.IntegerField()

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'last_name', 'patronimyc',  'age', 'city', 'photo',
                  'email', 'tel', 'sex', 'married',  'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SeekerRegisterForm, self).__init__(*args, **kwargs)
        blank_choice = (('', '----------'),)
        self.fields['username'] = forms.CharField(label='Ваш логин на портале')
        self.fields['password1'] = forms.CharField(label='Пароль', widget=forms.PasswordInput)
        self.fields['password2'] = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)
        self.fields['city'] = forms.CharField(label='Ваш город')
        self.fields['email'] = forms.EmailField(label='Ваш email')
        self.fields['tel'] = forms.CharField(label='Контактный тел.', validators=[
                    RegexValidator(regex='^8[0-9]{10}$', message='Допускаются только цифры '
                    'начиная с 8-ки, например 84952354422 или 89147900000.')])
        self.fields['sex'] = forms.ChoiceField(choices=blank_choice+Seeker.SEX_CHOICE,
                 label='Ваш пол')
        self.fields['married'] = forms.ChoiceField(choices=blank_choice+Seeker.MARRIED_STATUS,
                label='Ваше семейное положение')
        self.fields['first_name'] = forms.CharField(label='Фамилия')
        self.fields['last_name'] = forms.CharField(label='Имя')
        self.fields['patronimyc'] = forms.CharField(label='Отчество')
        self.fields['photo'] = forms.ImageField(label='Ваше фото', required=False,
                                                help_text='Поле необязательно')
        self.fields['age'] = forms.IntegerField(label='Ваш возраст', min_value=18, max_value=75)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды, для регистрации в качестве соискателя")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        email_db = User.objects.filter(email=data).first()
        if email_db:
            raise forms.ValidationError('Пользователь с такой электронной почтой уже зарегистрирован')
        return data


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label='Логин')
        self.fields['password'] = forms.CharField(label='Пароль', widget=forms.PasswordInput)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields['username'] = forms.CharField(label='Логин')
        self.fields['email'] = forms.EmailField(label='Ваш email')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserSeekerEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserSeekerEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields['username'] = forms.CharField(label='Логин')
        self.fields['first_name'] = forms.CharField(label='Фамилия')
        self.fields['last_name'] = forms.CharField(label='Имя')
        self.fields['email'] = forms.EmailField(label='Ваш email')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class EmployerEditForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('company_name', 'city', 'tel', 'web', 'logo', 'short_description')

    def __init__(self, *args, **kwargs):
        super(EmployerEditForm, self).__init__(*args, **kwargs)
        self.fields['tel'] = forms.CharField(label='Телефон компании', validators=[
            RegexValidator(regex='^8[0-9]{10}$', message='Допускаются только цифры '
                                                         'начиная с 8-ки, например 84952354422 или 89147900000.')])
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SeekerEditForm(forms.ModelForm):
    class Meta:
        model = Seeker
        fields = ('patronimyc', 'age', 'photo', 'city', 'tel', 'sex', 'married')

    def __init__(self, *args, **kwargs):
        super(SeekerEditForm, self).__init__(*args, **kwargs)
        self.fields['tel'] = forms.CharField(label='Контактный тел.', validators=[
            RegexValidator(regex='^8[0-9]{10}$', message='Допускаются только цифры '
                                                         'начиная с 8-ки, например 84952354422 или 89147900000.')])
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SetPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=32, label='введите новый пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, label='повторите пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2
