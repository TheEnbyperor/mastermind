from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('game/', game_create_view),
    path('game/<str:id>/', game_view),
    path('game/<str:id>/guesses/', game_guesses_view),
    path('game/<str:id>/guess/', game_guess_view),
]
