from django import forms
from .models import QuotesHonors, Comment, Category
from django.db import models
from author.models import Profile


class QuotesModelForm(forms.ModelForm):

    quotes = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'forms_quotes',
            'placeholder': 'Введите текст цитаты', }
    )
    )

    author = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'forms_author'
        }
    ),
        queryset=Profile.objects.all()
    )

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        to_field_name='title'
)

    class Meta:
        model = QuotesHonors
        fields = ('quotes', 'author', 'category', 'design')


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Add a comment'}))

    class Meta:
        model = Comment
        fields = ('body',)
