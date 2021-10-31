from django.urls import path

from .consumers import NewsSetupWebSocket, NewsSyncWebSocket
from .views import NewsListAPIView

urlpatterns = [
    path("", NewsListAPIView.as_view(), name="news_list"),
]

websockets_urlpatterns = [
    path("ws/news/syncing/", NewsSyncWebSocket.as_asgi()),
    path("ws/news/setup/", NewsSetupWebSocket.as_asgi()),
]
