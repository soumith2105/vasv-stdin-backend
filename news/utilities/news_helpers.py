from channels.db import database_sync_to_async

from news.models import News
from news.utilities.stores import get_saved_news
from vasvscrapper.news import get_news_in_range


async def fetch_news(start_page, end_page, increment=0, limit=20):
    last_news = await database_sync_to_async(News.objects.count)() != 0
    if last_news:
        last_news = await database_sync_to_async(News.objects.latest)("published_date")
    stop = False
    while not stop and start_page < limit:
        news = await get_news_in_range(start_page=start_page, end_page=end_page)
        start_page = end_page + 1
        end_page += increment
        stop = await get_saved_news(news_obj=news, last_news=last_news) or not bool(increment)
