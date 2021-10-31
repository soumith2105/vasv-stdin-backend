# from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncJsonWebsocketConsumer
# from rest_framework.authtoken.models import Token
#
# from students.utilities.starters import student_sync
#
#
# class StudentCreateWebSocket(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#
#     async def process(self, roll_number, password):
#         await student_sync(
#             roll_number=roll_number,
#             password=password,
#             fetch_type="create",
#             message=self.send_message,
#         )
#         await self.send_message("close", "Closing WebSocket")
#
#     async def receive_json(self, content, **kwargs):
#         roll_number = content["roll_number"]
#         password = content["password"]
#         await self.process(roll_number=roll_number, password=password)
#         await self.close()
#
#     async def send_message(self, status, message, code="", sync_type=""):
#         await self.send_json({"status": status, "message": message, "code": code, "type": sync_type})
#
#
# class StudentSyncNecessaryWebSocket(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#
#     @database_sync_to_async
#     def get_student_from_token(self, token):
#         return Token.objects.get(key=token).user
#
#     async def process(self, token):
#         student = await self.get_student_from_token(token)
#         await student_sync(
#             roll_number=student.roll_number,
#             password=student.std_pass,
#             fetch_type="syncing",
#             message=self.send_message,
#         )
#         await self.send_message("close", "Closing WebSocket")
#
#     async def receive_json(self, content, **kwargs):
#         token = content["token"]
#         await self.process(token)
#         await self.close()
#
#     async def send_message(self, status, message, code="", sync_type=""):
#         await self.send_json({"status": status, "message": message, "code": code, "type": sync_type})
