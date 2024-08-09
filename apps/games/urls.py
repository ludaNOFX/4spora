from django.urls import path, include
from rest_framework import routers
from .views import GameDetailView, RoomsList


urlpatterns = [
    path('rooms/', RoomsList.as_view(), name='rooms'),
    path('games/<int:room_id>/', GameDetailView.as_view(), name='game-detail'),

]