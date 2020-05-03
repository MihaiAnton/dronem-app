"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   03.05.2020 20:17
"""

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class RlConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_anonymus():
            await self.close()
        else:
            await self.accept()


