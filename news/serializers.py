from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            "id",
            "index",
            "published_date",
            "content",
            "link",
            "categories",
        ]

    def get_categories(self, obj: News):
        return obj.categories.strip("'][").split("', '")
