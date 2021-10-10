from django.urls import path

from employerapp import views


app_name = 'employerapp'

urlpatterns = [
    path('<int:emp_id>/', views.EmployerCabinetView.as_view(), name='cabinet'),
    path('<int:emp_id>/published/', views.VacancyPublishedView.as_view(), name='published'),
    path('<int:emp_id>/drafts/', views.VacancyDraftView.as_view(), name='drafts'),
    path('<int:emp_id>/messages/', views.MessagesView.as_view(), name='messages'),
    path('<int:emp_id>/hide/', views.VacancyHideView.as_view(), name='hide'),
    path('<int:emp_id>/vacancy_create/', views.CreateVacancyView.as_view(), name='vacancy_creation'),
    path('<int:emp_id>/vacancy_edit/<int:pk>/', views.VacancyEditView.as_view(), name='vacancy_edit'),
    path('<int:emp_id>/vacancy_delete/<int:pk>/', views.VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('<int:emp_id>/vacancy_view/<int:pk>/', views.VacancyDetailView.as_view(), name='vacancy_view'),
    path('<int:emp_id>/offer_for_resume/<int:pk>/', views.SendOfferCreateView.as_view(), name='send_offer'),
    path('<int:emp_id>/send_offers/', views.SendOffersView.as_view(), name='send_offers'),
    path('<int:emp_id>/offers/', views.MyOffersView.as_view(), name='offers'),
    path('company_profile/<int:emp_id>/', views.CompanyProfileView.as_view(), name='company_profile'),
    path('<int:emp_id>/favorites/', views.FavoritesResumeView.as_view(), name='favorites'),
    path('<int:emp_id>/delete_favorite/<int:pk>/', views.DeleteFavoriteResumeView.as_view(), name='delete_favorite'),
    path('offer_ajax/', views.offer_ajax, name='offer_ajax'),
    path('<int:emp_id>/search_resume/', views.SearchResumeListView.as_view(), name='search_resume')
]
