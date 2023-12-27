from django.urls import path
from .views import *

urlpatterns = [
    path('projects/', ProjectListView.as_view()),
    path('projects/<int:pk>', ProjectRetrieveView.as_view()),
    path('projects/<int:pk>/participation/', ParticipationCreateView.as_view()),
    path('participations/', ParticipationListView.as_view()),

]