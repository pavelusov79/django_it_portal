from django.urls import path

from workerapp import views

app_name = 'workerapp'

urlpatterns = [
    path('<int:seeker_id>/', views.worker_cabinet, name='seeker_cabinet'),
    path('<int:seeker_id>/search_vacancy/', views.search_vacancy, name='search_vacancy'),
    path('<int:seeker_id>/messages/', views.messages, name='messages'),
    path('<int:seeker_id>/drafts/', views.resume_drafts, name='drafts'),
    path('<int:seeker_id>/resume_published/', views.resume_published, name='published'),
    path('<int:seeker_id>/resume_hide/', views.hide_resumes, name='hide'),
    path('<int:seeker_id>/favorites_vacancies/', views.favorites, name='favorites'),
    path('<int:seeker_id>/create_resume/', views.create_resume, name='resume_creation'),
    path('<int:seeker_id>/edit_resume/<int:pk>/', views.resume_update, name='resume_update'),
    path('<int:seeker_id>/resume_delete/<int:pk>/', views.resume_delete, name='resume_delete'),
    path('<int:seeker_id>/resume_<int:resume_id>/experience_delete/<int:pk>/', views.resume_experience_delete,
         name='experience_delete'),
    path('<int:seeker_id>/resume_<int:resume_id>/education_delete/<int:pk>/', views.resume_education_delete,
         name='education_delete'),
    path('<int:seeker_id>/resume_view/<int:pk>/', views.resume_view, name='resume_view'),
    path('<int:seeker_id>/responses/', views.my_responses, name='responses'),
    path('<int:seeker_id>/response_for_vacancy/<int:pk>/', views.send_response, name='send_response'),
    path('<int:seeker_id>/send_responses/', views.send_responses, name='send_responses'),
    path('seeker_profile/<int:seeker_id>/', views.seeker_profile, name='seeker_profile'),
    path('<int:seeker_id>/delete_favorite/<int:pk>/', views.delete_favorite, name='delete_favorite'),
    path('response_ajax/', views.response_ajax, name="response_ajax")
]
