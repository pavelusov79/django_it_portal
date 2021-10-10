from django import forms
from django.core.validators import RegexValidator

from authapp.models import Employer
from employerapp.models import Vacancy, SendOffers


class VacancyCreationForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('vacancy_name', 'vacancy_type', 'city', 'min_salary', 'max_salary', 'currency',
                  'description', 'requirements', 'conditions', 'contact_person', 'contact_email',
                  'action')

        labels = {
            'action': 'Выберите действие',
        }

    def __init__(self, *args, **kwargs):
        super(VacancyCreationForm, self).__init__(*args, **kwargs)
        blank_choice = (('', '----------'),)
        action_choice = (
            ('draft', 'сохранить черновик'),
            ('publish', 'опубликовать на портале')
        )
        self.fields['action'] = forms.ChoiceField(label='Выберите действие',
                                                  choices=blank_choice + action_choice)
        self.fields['min_salary'] = forms.CharField(validators=[RegexValidator(regex='^[1-9]{1}['
            '0-9]{2,6}$', message='Для поля "минимальный уровень з/п" допускаются только цифры от 3-х до 7-ми '
             'цифр.')], label='Минимальный уровень з/п', help_text='Поле необязательно к '
                                                                   'заполнению', required=False)
        self.fields['max_salary'] = forms.CharField(validators=[RegexValidator(regex='^[1-9]{1}['
            '0-9]{2,6}$', message='Для поля "максимальный уровень з/п" допускаются только цифры '
            'от 3-х до 7-ми цифр.')], label='Максимальный уровень з/п', help_text='Поле '
            'необязательно к заполнению', required=False)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        min_salary = cleaned_data['min_salary']
        max_salary = cleaned_data['max_salary']
        currency = cleaned_data['currency']
        if min_salary and max_salary:
            if int(min_salary) > int(max_salary):
                raise forms.ValidationError({'max_salary': 'Максимальный уровень зп не может быть меньше минимального.'})
        if min_salary or max_salary:
            if not currency:
                raise forms.ValidationError({'currency': 'Введите валюту.'})
        return cleaned_data


class SendOfferForm(forms.ModelForm):
    class Meta:
        model = SendOffers
        fields = ('vacancy', 'cover_letter', 'contact_phone')

    def __init__(self, *args, **kwargs):
        if 'employer' in kwargs and kwargs['employer'] is not None:
            employer = kwargs.pop('employer')
            qs = Vacancy.objects.filter(action=Employer.MODER_OK, hide=False, employer=employer)
        super(SendOfferForm, self).__init__(*args, **kwargs)
        self.fields['vacancy'].queryset = qs
        self.fields['contact_phone'] = forms.CharField(label='контактный тел.',
            validators=[RegexValidator(regex='^8[0-9]{10}$', message='Допускаются только цифры '
            'начиная с 8-ки, например 84952354422 или 89147900000. ')],
                            help_text='поле необязательно к заполнению', required=False)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'




