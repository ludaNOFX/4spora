from django.urls import path
from .views import *

urlpatterns = [
    path('users/', GetAllUsers.as_view(), name='users-list'),
    path('create_room/', CreateRoom.as_view(), name='create-room'),
    path('rooms/', GetAllRooms.as_view(), name='rooms-list'),
    path('roombase/', GetAllRoomsBases.as_view(), name='room_base-list'),
    path('user/detail/<int:id>/', UserDetailInfo.as_view(), name='user-detail'),
    path('room/detail/<int:room_id>/', RoomDetailInfo.as_view(), name='room-detail'),
    path('base/detail/<int:id>/', RoomBaseDetailInfo.as_view(), name='room-base-detail'),
]