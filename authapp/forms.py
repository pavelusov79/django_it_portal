from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from authapp.models import Employer, Seeker


class EmployerRegisterForm(UserCreationForm):
    company_name = forms.CharField()
    tel = forms.IntegerField()
    web = forms.CharField()
    short_description = forms.CharField()
    logo = forms.ImageField(required=False)

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'company_name', 'email', 'web', 'tel', 'short_description',
                  'logo', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(EmployerRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label='Ваш логин на портале')
        self.fields['password1'] = forms.CharField(label='Пароль')
        self.fields['password2'] = forms.CharField(label='Подтвердите пароль')
        self.fields['email'] = forms.EmailField(label='Ваш email')
        self.fields['tel'] = forms.CharField(label='Телефон компании')
        self.fields['web'] = forms.CharField(label='Вебсайт компании')
        self.fields['short_description'] = forms.CharField(label='Краткое описание вашей компании')
        self.fields['logo'] = forms.ImageField(label='Ваш логотип', required=False,
                                               help_text='Поле необязательно')
        self.fields['company_name'] = forms.CharField(label='Название вашей компании')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SeekerRegisterForm(UserCreationForm):
    patronimyc = forms.CharField()
    tel = forms.CharField()
    hobby = forms.CharField()
    skills = forms.CharField()
    sex = forms.ChoiceField()
    married = forms.ChoiceField()
    photo = forms.ImageField()
    age = forms.IntegerField()

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'last_name', 'patronimyc',  'age', 'photo',  'email',
                  'tel', 'sex', 'married', 'skills', 'hobby',  'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SeekerRegisterForm, self).__init__(*args, **kwargs)
        blank_choice = (('', '----------'),)
        self.fields['username'] = forms.CharField(label='Ваш логин на портале')
        self.fields['password1'] = forms.CharField(label='Пароль')
        self.fields['password2'] = forms.CharField(label='Подтвердите пароль')
        self.fields['email'] = forms.EmailField(label='Ваш email')
        self.fields['tel'] = forms.CharField(label='Контактный тел.')
        self.fields['sex'] = forms.ChoiceField(choices=blank_choice+Seeker.SEX_CHOICE,
                 label='Ваш пол')
        self.fields['married'] = forms.ChoiceField(choices=blank_choice+Seeker.MARRIED_STATUS,
                label='Ваше семейное положение')
        self.fields['skills'] = forms.CharField(widget=forms.Textarea, label='Ваши навыки',
                required=False, max_length=264, help_text='Поле необязательно')
        self.fields['hobby'] = forms.CharField(widget=forms.Textarea, label='Ваши хобби',
                    required=False, max_length=264, help_text='Поле необязательно')
        self.fields['first_name'] = forms.CharField(label='Фамилия')
        self.fields['last_name'] = forms.CharField(label='Имя')
        self.fields['patronimyc'] = forms.CharField(label='Отчество')
        self.fields['photo'] = forms.ImageField(label='Ваше фото', required=False,
                                               help_text='Поле необязательно')
        self.fields['age'] = forms.IntegerField(label='Ваш возраст')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды, для регистрации в качестве соискателя")

        return data


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label='Логин')
        self.fields['password'] = forms.CharField(label='Пароль')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label='Логин')
        self.fields['email'] = forms.EmailField(label='Ваш email')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserSeekerEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserSeekerEditForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label='Логин')
        self.fields['first_name'] = forms.CharField(label='Фамилия')
        self.fields['last_name'] = forms.CharField(label='Имя')
        self.fields['email'] = forms.EmailField(label='Ваш email')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class EmployerEditForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('company_name', 'tel', 'web', 'logo', 'short_description')

    def __init__(self, *args, **kwargs):
        super(EmployerEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SeekerEditForm(forms.ModelForm):
    class Meta:
        model = Seeker
        fields = ('patronimyc', 'age', 'photo', 'tel', 'sex', 'married', 'hobby', 'skills')

    def __init__(self, *args, **kwargs):
        super(SeekerEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'