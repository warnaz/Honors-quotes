from django.db import models
from author.models import Profile
from django.db.models import Prefetch

# Create your models here.


class QuotesHonors(models.Model):
    DESIGN_CHOICE = [
        ('D1', 'Design one'),
        ('D2', 'Design two'),
        ('D3', 'Design three'),
    ]

    quotes = models.TextField()
    liked = models.ManyToManyField(Profile,
                                   related_name='likes_quotes', blank=True)
    editor = models.ForeignKey(Profile, on_delete=models.CASCADE,
                               related_name='quotes_editor')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,
                               related_name='quotes_author')
    category = models.ManyToManyField(
        'Category', related_name='quotes_category')
    design = models.CharField(
        max_length=2, choices=DESIGN_CHOICE, default='D1')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def number_comments(self):
        return self.quotes_comment.all().count()

    def get_category(self):
        x = self.category.all()
        ls = []
        for i in x:
            ls.append(i)

        return ls

    def __str__(self) -> str:
        return f'{str(self.quotes)}'

    class Meta:
        ordering = ('-created', )


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True)

    def __str__(self) -> str:
        return str(self.title)


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             related_name='user_like')
    quotes = models.ForeignKey(QuotesHonors, on_delete=models.CASCADE,
                               related_name='quotes_like')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'"{self.user}" like "{self.quotes}"'


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             related_name='user_comment', blank=True, null=True)
    quotes = models.ForeignKey(QuotesHonors, on_delete=models.CASCADE,
                               related_name='quotes_comment', blank=True, null=True, default=None)
    body = models.TextField(max_length=300)
    liked = models.ManyToManyField(Profile,
                                   related_name='likes_comment', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, default=None)

    def number_likes(self):
        return self.liked.all().count()

    def __str__(self) -> str:
        return f'"{self.user}" comment "{self.quotes}"'

    class Meta:
        ordering = ('-created', )


class CommentLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             related_name='user_comment_like')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                related_name='comment_like')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'"{self.user}" лайкнул комментарий "{self.comment}"'
