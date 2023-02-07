from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from quotes.models import Comment, CommentLike, Like, QuotesHonors
from author.models import Profile
from quotes.forms import QuotesModelForm, CommentModelForm
import json


def create_comment(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        data = json.loads(request.body)
        post_id = data['post_id']
        comment_body = data['body']
        quotes = get_object_or_404(QuotesHonors, id=post_id)
        comment = Comment.objects.create(
            user=profile,
            body=comment_body,
            quotes=quotes
        )

        return JsonResponse({
            'body': comment.body,
            'first_name': comment.user.first_name,
            'last_name': comment.user.last_name
        })


def create_like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        quotes_obj = QuotesHonors.objects.get(pk=post_id)
        profile = Profile.objects.get(user=request.user)

        if quotes_obj.liked.contains(profile):
            quotes_obj.liked.remove(profile)
        else:
            quotes_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(
            user=profile, quotes_id=post_id)

        liked = False

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        quotes_obj.save()

    return JsonResponse({
        'liked': liked
    })


def create_comment_like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment_obj = Comment.objects.get(pk=post_id)
        profile = Profile.objects.get(user=request.user)

        if profile in comment_obj.liked.all():
            comment_obj.liked.remove(profile)
        else:
            comment_obj.liked.add(profile)

        like, created = CommentLike.objects.get_or_create(
            user=profile, comment_id=post_id)

        comment_liked = False

        if not created:
            like.delete()
            comment_liked = False
        else:
            comment_liked = True

        comment_obj.save()

    return JsonResponse({
        'comment_liked': comment_liked
    })
