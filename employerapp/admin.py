from django import forms
from django.contrib import admin

from employerapp.models import Vacancy


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ('failed', 'is_active', 'is_favorite')

    def __init__(self, *args, **kwargs):
        super(VacancyForm, self).__init__(*args, **kwargs)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('vacancy_name', 'employer', 'action')
    list_filter = ('action', )
    form = VacancyForm
