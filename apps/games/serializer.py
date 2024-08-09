from rest_framework import serializers
from .models import Room, RoomBase


class RoomsSerailzier(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["players"]

    def update(self, instance, validated_data):
        instance.players = validated_data.get('players', instance.players)
        instance.save()
        return instance


class GameSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'room_name', 'players']

    def get_players(self, obj):
        player_rooms = Room.objects.filter(room=obj).order_by('joined_at')
        return [player_room.player.id for player_room in player_rooms]


class RoomBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBase
        fields = "__all__"
