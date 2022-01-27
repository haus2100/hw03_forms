from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text':'текст',
            'group':'группа'
        }
        help_texts = {
            'text':'все что угодно',
            'group':'из муществующих'
        }
