from django.urls import path

from workerapp import views

app_name = 'workerapp'

urlpatterns = [
    path('<int:seeker_id>/', views.WorkerCabinetView.as_view(), name='seeker_cabinet'),
    path('<int:seeker_id>/search_vacancy/', views.SearchVacancyListView.as_view(), name='search_vacancy'),
    path('<int:seeker_id>/messages/', views.MessagesView.as_view(), name='messages'),
    path('<int:seeker_id>/drafts/', views.ResumeDraftsView.as_view(), name='drafts'),
    path('<int:seeker_id>/resume_published/', views.PublishedResumesView.as_view(), name='published'),
    path('<int:seeker_id>/resume_hide/', views.HideResumesView.as_view(), name='hide'),
    path('<int:seeker_id>/favorites_vacancies/', views.FavoriteVacanciesView.as_view(), name='favorites'),
    path('<int:seeker_id>/create_resume/', views.ResumeCreateView.as_view(), name='resume_creation'),
    path('<int:seeker_id>/edit_resume/<int:pk>/', views.ResumeUpdateView.as_view(), name='resume_update'),
    path('<int:seeker_id>/resume_delete/<int:pk>/', views.DeleteResumeView.as_view(), name='resume_delete'),
    path('<int:seeker_id>/resume_<int:resume_id>/experience_delete/<int:pk>/',
         views.ResumeExperienceDeleteView.as_view(), name='experience_delete'),
    path('<int:seeker_id>/resume_<int:resume_id>/education_delete/<int:pk>/', views.ResumeEducationDeleteView.as_view(),
         name='education_delete'),
    path('<int:seeker_id>/resume_view/<int:pk>/', views.ResumeDetailView.as_view(), name='resume_view'),
    path('<int:seeker_id>/responses/', views.MyResponsesView.as_view(), name='responses'),
    path('<int:seeker_id>/response_for_vacancy/<int:pk>/', views.SendResponseCreateView.as_view(),
         name='send_response'),
    path('<int:seeker_id>/send_responses/', views.SendResponsesView.as_view(), name='send_responses'),
    path('seeker_profile/<int:seeker_id>/', views.SeekerProfileView.as_view(), name='seeker_profile'),
    path('<int:seeker_id>/delete_favorite/<int:pk>/', views.FavoriteVacancyDeleteView.as_view(),
         name='delete_favorite'),
    path('response_ajax/', views.response_ajax, name="response_ajax")
]
