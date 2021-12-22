from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('surveys/', views.SurveyList.as_view()),
    path('surveys/<int:pk>/', views.SurveyDetail.as_view()),
    path('getactivesurveys/', views.ActiveSurveyList.as_view()),
    path('getpid/', views.ParticipantCreate.as_view()),
    path('answers/<pk>/', views.AnswerList.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
