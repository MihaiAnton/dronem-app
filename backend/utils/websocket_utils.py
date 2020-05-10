"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   09.05.2020 13:38
"""
from typing import Dict

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_to_websocket(data: Dict, room_name: str):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(room_name, {'type': 'send_message', 'data': data})
