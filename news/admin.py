from django.contrib import admin
from django.utils.html import format_html

from vasvscrapper.enums import NewsPatternsEnum
from .models import News


class TypeOfNews(admin.SimpleListFilter):
    title = "Type"
    parameter_name = "type"

    def lookups(self, request, model_admin):
        return NewsPatternsEnum.get_news_keys()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.distinct().filter(categories__contains=self.value())


class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "published_date",
        "index",
        "show_content_url",
    )
    search_fields = (
        "published_date",
        "index",
        "content",
    )
    list_filter = (
        "published_date",
        TypeOfNews,
    )

    def show_content_url(self, obj):
        return format_html('<p style="width:max(500px);"><a href="%s">%s</a></p>' % (obj.link, obj.content))

    show_content_url.allow_tags = True
    show_content_url.short_description = "Content"


admin.site.register(News, NewsAdmin)
