from django.contrib import admin
from django.contrib.admin import StackedInline

from workerapp.models import Resume, ResumeExperience, ResumeEducation


def name(obj):
    return f'{obj.seeker.user.first_name} {obj.seeker.user.last_name} {obj.seeker.patronimyc}'


class ResumeExperienceInline(StackedInline):
    model = ResumeExperience
    exclude = ('is_active',)
    extra = 0


class ResumeEducationInline(StackedInline):
    model = ResumeEducation
    exclude = ('is_active',)
    extra = 0


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (name, 'position', 'action')
    list_filter = ('action', )
    inlines = [ResumeEducationInline, ResumeExperienceInline]
    fieldsets = (
        ('Раздел модерации', {
            'fields': ('action', 'failed_moderation')
        }),
        ('Общая информация', {
            'fields': ('seeker', 'position', ('min_salary', 'max_salary', 'currency'),
                        'skills', 'hobby')

        })
    )
