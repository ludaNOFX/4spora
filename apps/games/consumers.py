# # games/consumers.py
#
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
#
# class GameConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         from .models import Room  # Импорт модели внутри метода
#         self.room_id = self.scope['url_route']['kwargs']['room_id']
#         self.room_group_name = f'game_{self.room_id}'
#
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         from .models import Room  # Импорт модели внутри метода
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'game_message',
#                 'message': message
#             }
#         )
#
#     async def game_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
#
#     async def send_game_info(self):
#         from .models import Room  # Импорт модели внутри метода
#         room = Room.objects.get(id=self.room_id)
#         room_info = {
#             'room_name': room.room_name,
#             'player_count': room.current_player_count()
#         }
#
#         # Send room information to the client
#         await self.send(text_data=json.dumps(room_info))


# games/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room
from asgiref.sync import sync_to_async  # Импорт sync_to_async

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'game_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send initial game information when connection is established
        await self.send_game_info(self.room_id)  # Передаем room_id в качестве аргумента

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle receiving messages, if needed
        pass

    async def send_game_info(self, room_id):  # Принимаем room_id в качестве аргумента
        # Fetch room information from database asynchronously
        room = await self.get_room_info(room_id)  # Передаем room_id в качестве аргумента
        players = await self.get_current_players(room_id)
        room_info = {
            'room_name': room.room_name,
            'player_count': await self.current_player_count(room_id),  # Используем sync_to_async
            'players': players  # Оставляем эту часть без изменений
        }

        # Отправляем информацию об игре только после завершения всех асинхронных вызовов
        await self.send(text_data=json.dumps(room_info))

    # Асинхронная функция для получения информации о комнате из базы данных
    @sync_to_async
    def get_room_info(self, room_id):  # Исправлено на self
        return Room.objects.get(id=room_id)

    # Асинхронная функция для получения текущих игроков из базы данных
    @sync_to_async
    def get_current_players(self, room_id):  # Исправлено на self
        room = Room.objects.get(id=room_id)
        return [player.username for player in room.players.all()]  # Мы получаем список имен игроков

    # Асинхронная функция для получения количества текущих игроков из базы данных
    @sync_to_async
    def current_player_count(self, room_id):  # Исправлено на self
        room = Room.objects.get(id=room_id)
        return room.players.count()
