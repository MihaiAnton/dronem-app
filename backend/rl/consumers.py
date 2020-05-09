"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   03.05.2020 20:17
"""
import json

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer


class RlConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['group_id']
        print(f'RLTrainConsumer - connect {self.room_name}')

        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        print(f'RLTrainConsumer - disconnect')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        raise StopConsumer()

    def send_message(self, event):
        print(f'RLTrainConsumer - send_message {event} on room {self.room_name}')
        if event.get('end', False):
            self.send(json.dumps(event))
            self.disconnect(0)
            return
        self.send(json.dumps(event))

    def receive(self, text_data=None, bytes_data=None):
        print("RLTrainConsumer - receive")
        pass
