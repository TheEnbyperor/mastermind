from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('game/<str:id>/', game_view),
]
