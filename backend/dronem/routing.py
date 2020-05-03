"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   03.05.2020 18:57
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from rl.consumers import RlConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('test/', RlConsumer)
        ])
    )
})
