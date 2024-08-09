from datetime import datetime
from decimal import Decimal
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404, render
from rest_framework import status, permissions, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Room, RoomBase, RoomPlayer
from .serializer import RoomsSerailzier, RoomInSerializer
from ..users.models import MainUser


# class RoomsViewSet(viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomsSerailzier


class RoomsList(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomsSerailzier


class GameDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, room_id):
        game = get_object_or_404(Room, id=room_id)
        serializer = RoomsSerailzier(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_id):
        game = get_object_or_404(Room, id=room_id)
        user = request.user

        if user not in game.players.all():
            if user.deduct_balance(Decimal(game.game_amount)):
                RoomPlayer.add_player_to_room(game, user)

                if game.current_player_count() >= game.max_players:
                    game.players.order_by('roomplayer__join_order')
                    losers = game.determine_losers()
                    if losers:
                        loser_ids = [loser.id for loser in losers]
                        winners = game.players.exclude(id__in=loser_ids)
                        winner_ids = [winner.id for winner in winners]
                        losers = game.players.filter(id__in=loser_ids)

                        total_amount = Decimal(game.game_amount) * game.current_player_count()
                        commission = total_amount * Decimal('0.10')  # 10% комиссия
                        remaining_amount = total_amount - commission
                        loser_share = remaining_amount * Decimal('0.10')
                        print(f'Total amount {total_amount}')
                        print(f'commision {commission}')
                        print(f'remaining amount {remaining_amount}')
                        print(f'loser share {loser_share}')

                        # Распределение баланса между победителями
                        winner_share = (remaining_amount - loser_share) / winners.count()
                        print(f'Winner {winner_share}')
                        for winner in winners:
                            winner.add_balance(winner_share)
                            winner.winrate += 1
                            winner.tokenswin += winner_share
                            winner.save()

                        # Обработка проигравших
                        for loser in losers:
                            loser.add_balance(loser_share)  # Возвращаем часть ставки
                            loser.loserate += 1
                            loser.tokenslose += (Decimal(game.game_amount) - loser_share)  # Записываем потерю
                            loser.save()

                        game_info = RoomBase.objects.create(
                            room_id=room_id,
                            room_max_players=game.max_players,
                            room_game_amount=game.game_amount,
                            room_loser_rule=game.loser_rule,
                            date_time=datetime.now(),
                            commission=commission,
                        )
                        game_info.room_players.set(game.players.all())
                        game_info.winners.set(winners)
                        game_info.losers.set(losers)
                        game_info.save()

                        game.clear_players()

                        # Отправка сообщения через WebSocket
                        channel_layer = get_channel_layer()
                        async_to_sync(channel_layer.group_send)(
                            f'game_{room_id}',
                            {
                                'type': 'game_message',
                                'message': f'Игра завершена. Проигравшие: {loser_ids}, Победители: {winner_ids}, Комиссия: {commission}'
                            }
                        )

                        return Response(
                            {'message': f'Игра завершена. Проигравшие: {loser_ids}', 'winners': winner_ids, 'commission': commission},
                            status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {'message': 'Игра началась. Ожидаем следующих игроков.'},
                            status=status.HTTP_200_OK
                        )
                else:
                    return Response(
                        {'message': f'Игрок добавлен. Ожидаем следующих игроков. ({game.current_player_count()}/{game.max_players})'},
                        status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    {'message': 'Недостаточно средств для вступления в игру'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'message': 'Пользователь уже участвует в игре'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, room_id):
        try:
            mainuser = request.user
            game = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'Комната не найдена'}, status=status.HTTP_404_NOT_FOUND)

        if game.players.filter(id=mainuser.id).exists():
            mainuser.add_balance(game.game_amount)
            game.players.remove(mainuser)
            game.save()
            mainuser.save()

            serializer = RoomsSerailzier(game, data={}, partial=True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Что то пошло не так попробуйте еще раз"}, status=status.HTTP_400_BAD_REQUEST)





