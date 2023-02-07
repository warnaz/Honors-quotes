from django.contrib import admin
from .models import QuotesHonors, Like, Comment, Category, CommentLike
# Register your models here.
admin.site.register(QuotesHonors)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(CommentLike)
