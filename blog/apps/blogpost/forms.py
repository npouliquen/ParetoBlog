from django import forms

from .models import Post
from markdownx.models import MarkdownxField


class PostForm(forms.ModelForm):

    markdown = MarkdownxField()

    class Meta:
        model = Post
        fields = ('title', 'text')
