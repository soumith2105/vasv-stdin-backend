from channels.generic.websocket import AsyncJsonWebsocketConsumer

from news.utilities.news_helpers import fetch_news


class NewsSetupWebSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await fetch_news(1, 20)
        await self.send_message("success", "Done")
        await self.close()

    async def send_message(self, message_type, message):
        await self.send_json({"type": message_type, "message": message})


class NewsSyncWebSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await fetch_news(1, 2, increment=2)
        await self.send_message("success", "Done")
        await self.close()

    async def send_message(self, message_type, message):
        await self.send_json({"type": message_type, "message": message})
