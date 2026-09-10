from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('squads/', views.squads, name='squads'),
    path('sports/ai/', views.ai_analysis, name='ai_analysis'),
    path('sports/match/', views.match_centre, name='match_centre'),
    path('sports/live/', views.live_dashboard, name='live_dashboard'),
    path('sports/team/', views.team_page, name='team_page'),
    path('sports/player/', views.player_page, name='player_page'),
    path('sports/picks/', views.my_picks, name='my_picks'),
]
