from random import choice
from string import ascii_letters, digits

from django.db import models


def generate_id():
    n = 8
    random = ascii_letters + digits + "_"
    return "".join(choice(random) for _ in range(n))


class News(models.Model):
    index = models.CharField(max_length=50, null=False, blank=False)
    published_date = models.DateField()
    content = models.TextField()
    slug = models.SlugField(unique=True, default=generate_id, null=False, blank=False)
    link = models.URLField(max_length=300, null=False, blank=False)
    categories = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        ordering = [
            "-published_date",
        ]
        verbose_name_plural = "News"

    def __str__(self):
        return f"{self.content[:30]}..."
