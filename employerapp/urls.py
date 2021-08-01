from django.urls import path

from employerapp import views

app_name = 'employerapp'

urlpatterns = [
    path('<int:emp_id>/', views.employer_cabinet, name='cabinet'),
    path('<int:emp_id>/published/', views.vacancy_published, name='published'),
    path('<int:emp_id>/drafts/', views.vacancy_draft, name='drafts'),
    path('<int:emp_id>/messages/', views.messages, name='messages'),
    path('<int:emp_id>/hide/', views.vacancy_hide, name='hide'),
    path('<int:emp_id>/vacancy_create/', views.creation, name='vacancy_creation'),
    path('<int:emp_id>/vacancy_draft_edit/<int:pk>/', views.vacancy_edit_draft,
         name='vacancy_edit_draft'),
    path('<int:emp_id>/vacancy_edit/<int:pk>/', views.vacancy_edit, name='vacancy_edit'),
    path('<int:emp_id>/vacancy_delete/<int:pk>/', views.vacancy_delete, name='vacancy_delete'),
    path('<int:emp_id>/vacancy_view/<int:pk>/', views.vacancy_view, name='vacancy_view'),
    path('<int:emp_id>/offer_for_resume/<int:pk>/', views.send_offer, name='send_offer'),
    path('<int:emp_id>/send_offers/', views.send_offers, name='send_offers'),
    path('<int:emp_id>/offers/', views.my_offers, name='offers'),
    path('company_profile/<int:emp_id>/', views.company_profile, name='company_profile'),
    path('<int:emp_id>/favorites/', views.favorites_resume, name='favorites'),
    path('<int:emp_id>/delete_favorite/<int:pk>/', views.delete_favorite, name='delete_favorite'),
    path('offer_ajax/', views.offer_ajax, name='offer_ajax'),
    path('<int:emp_id>/search_resume/', views.search_resume, name='search_resume')
]
