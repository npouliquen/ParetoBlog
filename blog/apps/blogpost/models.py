from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from markdownx.models import MarkdownxField


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = MarkdownxField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def get_image(self):
        index = self.text.find("![]")
        if (index > -1):
            start_of_url = index + 4
            end_of_url = self.text.find(')', start_of_url)
            url = self.text[start_of_url:end_of_url]
            return url
        else:
            return "https://s3.amazonaws.com/paretoengineeringblog/ParetoLogo1.png"

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
