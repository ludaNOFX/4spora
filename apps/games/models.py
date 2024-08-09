from django.db import models
from apps.users.models import MainUser
import random
from decimal import Decimal


class Room(models.Model):
    room_name = models.CharField(max_length=50)
    players = models.ManyToManyField(MainUser, through='RoomPlayer', related_name='rooms', blank=True)
    max_players = models.IntegerField(default=4)  # Поле для хранения максимального количества игроков
    loser_rule = models.IntegerField(default=4)  # Поле для хранения правила (каждый N-ый игрок проигрывает)
    game_amount = models.IntegerField(default=10)

    def current_player_count(self):
        return self.roomplayer_set.count()

    # def current_player_count(self):
    #     return self.players.count()

    def determine_losers(self):
        # Определение игроков, которые проиграли по правилу "каждый N-ый игрок проигрывает"
        current_count = self.current_player_count()
        if current_count >= self.max_players:
            players_list = list(self.players.all().order_by('roomplayer__join_order'))
            # Выбор проигравших игроков согласно правилу (N-ый игрок)
            print()
            print()
            print()
            print()
            print(self.loser_rule)
            print(list(enumerate(players_list)))
            print()
            print()
            print()
            print()
            losers = [player for idx, player in enumerate(players_list)
                      if (idx + 1) == self.loser_rule]
            return losers
        return None

    def clear_players(self):
        self.players.clear()
        self.save()

    def __str__(self):
        return self.room_name


class RoomPlayer(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    player = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    join_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['join_order']
        unique_together = ('room', 'player')

    def add_player_to_room(room, player):
        join_order = RoomPlayer.objects.filter(room=room).count() + 1
        RoomPlayer.objects.create(room=room, player=player, join_order=join_order)


class RoomBase(models.Model):
    room_id = models.IntegerField()
    room_players = models.ManyToManyField(MainUser, related_name='room_players', blank=True)
    room_max_players = models.IntegerField(default=4)
    room_loser_rule = models.IntegerField(default=4)
    room_game_amount = models.IntegerField(default=10)
    winners = models.ManyToManyField(MainUser, related_name='winners', blank=True)
    losers = models.ManyToManyField(MainUser, related_name='losers', blank=True)
    date_time = models.DateTimeField()
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

