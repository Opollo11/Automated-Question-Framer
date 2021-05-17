from django.contrib import admin
from django.urls import path
from .views import audioToQuestions
urlpatterns = [
    path('', audioToQuestions,name='audio-to-questions')
]
