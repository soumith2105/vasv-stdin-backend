from channels.db import database_sync_to_async

from news.models import News


@database_sync_to_async
def get_saved_news(news_obj, last_news):
    stop = False
    creations = []
    for news in news_obj:
        new_news = News(
            published_date=news["date"],
            content=news["content"],
            index=news["index"],
            link=news["link"],
            categories=news["categories"],
        )
        if last_news:
            if str(new_news.published_date) == str(last_news.published_date) and new_news.content == last_news.content:
                stop = True
                break
        creations.append(new_news)

    News.objects.bulk_create(creations)
    return stop
