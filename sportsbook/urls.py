from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('squads/', views.squads, name='squads'),
    path('sports/ai/', views.ai_analysis, name='ai_analysis'),
]
