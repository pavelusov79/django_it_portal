from django.contrib import admin
from django.core.mail import send_mail
from django import forms

from authapp.models import Employer, Seeker


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmployerForm, self).__init__(*args, **kwargs)
        self.fields['failed_moderation'] = forms.CharField(max_length=512, label='поле в случае '
            'отклонения модерации', widget=forms.Textarea(attrs={'rows': 5}), required=False)

    def clean_status(self):
        status = self.cleaned_data.get('status')
        company_name = self.cleaned_data.get('company_name')
        user = self.cleaned_data.get('user')
        if status == 'moderation_ok':
            send_mail('статус модерации на портале IT Recrut', f'Ваша компания '
                    f'{company_name} успешно прошла модерацию. Теперь вы '
                    f'можете размещать свои вакансии.', 'it.portal.gb@gmail.com',
                      [user.email,])
        return status

    def clean_failed_moderation(self):
        failed_text = self.cleaned_data.get('failed_moderation')
        status = self.cleaned_data.get('status')
        user = self.cleaned_data.get('user')
        if status == "moderation_reject":
            if not failed_text:
                raise forms.ValidationError('вы должны заполнить поле "в случае отклонения '
                                            'модерации"')
            send_mail('статус модерации на портале IT Recrut', f'Вы не прошли модера'
            f'цию. {failed_text}', 'it.portal.gb@gmail.com', [user.email, ])

        return failed_text


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'status',)
    list_filter = ('status', )
    form = EmployerForm


class SeekerForm(forms.ModelForm):
    class Meta:
        model = Seeker
        exclude = ('skills', 'hobby',)

    def __init__(self, *args, **kwargs):
        super(SeekerForm, self).__init__(*args, **kwargs)
        self.fields['failed_moderation'] = forms.CharField(max_length=512, label='поле в случае '
            'отклонения модерации', widget=forms.Textarea(attrs={'rows': 5}), required=False)

    def clean_status(self):
        status = self.cleaned_data.get('status')
        user = self.cleaned_data.get('user')
        if status == 'moderation_ok':
            send_mail('статус модерации на портале IT Recrut', f'Вы успешно прошли модерацию. '
            f'Теперь вы можете размещать свои резюме.', 'it.portal.gb@gmail.com', [user.email, ])
        return status

    def clean_failed_moderation(self):
        failed_text = self.cleaned_data.get('failed_moderation')
        status = self.cleaned_data.get('status')
        user = self.cleaned_data.get('user')
        if status == "moderation_reject":
            if not failed_text:
                raise forms.ValidationError('вы должны заполнить поле "в случае отклонения '
                                            'модерации"')
            send_mail('статус модерации на портале IT Recrut', failed_text,
                      'it.portal.gb@gmail.com', [user.email, ])
        return failed_text


def name(obj):
    return f'{obj.user.first_name} {obj.user.last_name} {obj.patronimyc}'


@admin.register(Seeker)
class SeekerAdmin(admin.ModelAdmin):
    list_display = (name, 'status', )
    list_filter = ('status',)
    form = SeekerForm

