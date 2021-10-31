from rest_framework.generics import ListAPIView

from .models import News
from .pagination import NewsPagination
from .serializers import NewsSerializer


class NewsListAPIView(ListAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    pagination_class = NewsPagination

    class Meta:
        model = News
