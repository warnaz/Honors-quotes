from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from quotes.models import Comment, CommentLike, Like, QuotesHonors
from author.models import Profile
from quotes.forms import QuotesModelForm, CommentModelForm
import json
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from quotes.models import (
    QuotesHonors,
    Comment
)
from author.models import Profile
from django.db.models import Q
from django.views.generic import DetailView, DeleteView, UpdateView
from quotes.forms import QuotesModelForm, CommentModelForm
import json
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from services import queryset


def create_quote(request):
    profile = Profile.objects.get(user=request.user)
    quote_form = QuotesModelForm(request.POST, request.FILES)
    if quote_form.is_valid():
        instance = quote_form.save(commit=False)
        instance.editor = profile
        instance.save()
        quote_form.save_m2m()
        quote_form = QuotesModelForm()

