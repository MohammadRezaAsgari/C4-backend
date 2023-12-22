from django.urls import path
from .views import *

urlpatterns = [
    path('projects/', ProjectListView.as_view()),

]