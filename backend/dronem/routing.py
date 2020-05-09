"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   03.05.2020 18:57
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
import rl.consumers

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/train_updates/(?P<group_id>\w+)/$', rl.consumers.RlConsumer)
        ])
    )
})
