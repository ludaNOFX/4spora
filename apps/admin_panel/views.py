from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.games.models import Room, RoomBase
from apps.games.serializer import RoomsSerailzier, RoomBaseSerializer
from apps.users.models import MainUser
from apps.users.serializer import MainUserSerializerData


class CreateRoom(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = RoomsSerailzier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Комната создана.'},
                            status=status.HTTP_201_CREATED)


class GetAllUsers(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = MainUser.objects.all()
    serializer_class = MainUserSerializerData


class GetAllRooms(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Room.objects.all()
    serializer_class = RoomsSerailzier


class GetAllRoomsBases(ListAPIView):
    permissions = [permissions.IsAdminUser]
    queryset = RoomBase.objects.all()
    serializer_class = RoomBaseSerializer


class UserDetailInfo(APIView):
    permissions = [permissions.IsAdminUser]

    def get(self, request, id):
        user = get_object_or_404(MainUser, id=id)
        serializer = MainUserSerializerData(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        user = get_object_or_404(MainUser, id=id)
        serializer = MainUserSerializerData(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = get_object_or_404(MainUser, id=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomDetailInfo(APIView):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        serializer = RoomsSerailzier(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        serializer = RoomsSerailzier(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomBaseDetailInfo(APIView):
    def get(self, request, id):
        base = get_object_or_404(RoomBase, id=id)
        serializer = RoomBaseSerializer(base)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        base = get_object_or_404(RoomBase, id=id)
        serializer = RoomBaseSerializer(base, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        base = get_object_or_404(RoomBase, id=id)
        base.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
