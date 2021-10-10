from django import forms
from django.core.validators import RegexValidator

from workerapp.models import Resume, ResumeEducation, ResumeExperience, SendResponse


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('position', 'min_salary', 'max_salary', 'currency', 'skills', 'hobby', 'action')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        blank_choice = (('', '----------'),)
        status_choice = (
            ('draft', 'сохранить черновик'),
            ('publish', 'опубликовать на портале')
        )
        self.fields['action'] = forms.ChoiceField(label='Выберите действие',
                                                  choices=blank_choice + status_choice)
        self.fields['skills'] = forms.CharField(label='Ключевые навыки', max_length=512,
                                                widget=forms.Textarea(attrs={'rows': 4}))
        self.fields['hobby'] = forms.CharField(label='Ваши увлечения', max_length=512,
            widget=forms.Textarea(attrs={'rows': 4}), help_text='поле необязательное', required=False)
        self.fields['min_salary'] = forms.CharField(validators=[RegexValidator(regex='^[1-9]{1}[0-9]{2,6}$',
            message='Для поля "минимальный уровень з/п" допускаются только цифры от 3-х до 7-ми цифр.')],
            label='Минимальный уровень з/п', help_text='Поле необязательно к заполнению', required=False)
        self.fields['max_salary'] = forms.CharField(validators=[RegexValidator(regex='^[1-9]{1}[0-9]{2,6}$',
            message='Для поля "максимальный уровень з/п" допускаются только цифры от 3-х до 7-ми цифр.')],
            label='Максимальный уровень з/п', help_text='Поле необязательно к заполнению', required=False)
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


class ResumeEducationForm(forms.ModelForm):
    class Meta:
        model = ResumeEducation
        fields = ('edu_type', 'degree', 'institution_name', 'from_date', 'to_date', 'course_name',
                  'edu_description')

        class DateInput(forms.DateInput):
            input_type = 'date'

        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput()
        }

        labels = {
            'from_date': 'Дата начала',
            'to_date': 'Дата окончания'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        blank_choice = (('', '----------'),)
        self.fields['edu_type'] = forms.ChoiceField(label='Тип образования',
                                                    choices=blank_choice+ResumeEducation.EDU_TYPE_CHOICES)
        self.fields['degree'] = forms.ChoiceField(label='Уровень',
                                                  choices=blank_choice+ResumeEducation.DEGREE_CHOICES)
        self.fields['edu_description'] = forms.CharField(label='Описание', max_length=512,
            widget=forms.Textarea(attrs={'rows': 4}), required=False , help_text='поле необязательное')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_to_date(self):
        from_date = self.cleaned_data.get('from_date')
        to_date = self.cleaned_data.get('to_date')
        if to_date and from_date and to_date < from_date:
            raise forms.ValidationError('Дата окончания обучения не должна быть раньше даты начала.')
        return to_date


class ResumeExperienceForm(forms.ModelForm):
    class Meta:
        model = ResumeExperience
        fields = ('company_name', 'job_title', 'start_date', 'finish_date', 'job_description')

        class DateInput(forms.DateInput):
            input_type = 'date'

        widgets = {
            'start_date': DateInput(),
            'finish_date': DateInput()
        }

        labels = {
            'start_date': 'Дата начала работы',
            'finish_date': 'Дата окончания работы'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job_description'] = forms.CharField(label='Описание обязанностей', max_length=512,
            widget=forms.Textarea(attrs={'rows': 4}), help_text='Поле необязательное', required=False)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_finish_date(self):
        start_date = self.cleaned_data.get('start_date')
        finish_date = self.cleaned_data.get('finish_date')
        if start_date and finish_date:
            if finish_date < start_date:
                raise forms.ValidationError('Дата окончания работы в данном месте работы не может быть раньше даты начала.')
        return finish_date


class SendResponseForm(forms.ModelForm):
    class Meta:
        model = SendResponse
        fields = ('resume', 'cover_letter', )

    def __init__(self, *args, **kwargs):
        if 'seeker' in kwargs and kwargs['seeker'] is not None:
            seeker = kwargs.pop('seeker')
            resume_list = Resume.objects.filter(seeker=seeker, action='moderation_ok', hide=False)
            super(SendResponseForm, self).__init__(*args, **kwargs)
            self.fields['resume'].queryset = resume_list
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'