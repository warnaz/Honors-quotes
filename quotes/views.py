from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import (
    QuotesHonors,
    Comment
)
from author.models import Profile
from django.db.models import Q
from django.views.generic import DetailView, DeleteView, UpdateView
from .forms import QuotesModelForm, CommentModelForm
import json
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from services import queryset
from quotes.business.quotes_logic import create_quote
# Create your views here.


@login_required
def create_view(request):
    quote_form = QuotesModelForm()
    comment_form = CommentModelForm()
    user = queryset.get_profile(request.user)

    if 'submit_p_form' in request.POST:
        create_quote(request)
        return redirect("love:home_urls")
    context = {
        'quote_form': quote_form,
        'comment_form': comment_form,
        'user': user,
    }

    return render(request, 'quotes/main.html', context)


def search(request):
    search = request.GET.get('q', '')
    qs_prof = Profile.objects.filter(Q(first_name__icontains=search) |
                                     Q(last_name__icontains=search) |
                                     Q(user__username=search))
    user = Profile.objects.get(user=request.user)

    return render(request, 'quotes/search.html', {'user': user, 'qs_prof': qs_prof})


class QuotesDetail(DetailView):
    model = QuotesHonors
    template_name = 'quotes/quotes_detail.html'

    def get(self, request, *args, **kwargs):
        kp = self.kwargs.get('pk')
        post = QuotesHonors.objects.prefetch_related(
            Prefetch(
                'quotes_comment',
                queryset=Comment.objects.prefetch_related('liked'))
        ).select_related('author', 'editor').prefetch_related('liked').get(pk=kp)

        user = Profile.objects.get(user=request.user)

        context = {
            'post': post,
            'user': user
        }
        return render(request, self.template_name, context)


class AuthorQuotes(DetailView):
    template_name = 'quotes/users_quotes/author.html'

    def get(self, request, *args, **kwargs):
        user = Profile.objects.get(user=request.user)
        kp = self.kwargs.get('slug')
        user_slug = Profile.objects.get(slug=kp)

        context = {
            'user': user,
            'user_slug': user_slug,
        }

        return render(request, self.template_name, context)


class EditorQuotes(AuthorQuotes):
    template_name = 'quotes/users_quotes/editor.html'


class ChangeQuotes(DetailView):
    template_name = 'quotes/users_quotes/change_quotes.html'

    def get(self, request, *args, **kwargs):
        user = Profile.objects.get(user=request.user)
        kp = self.kwargs.get('id')
        post = QuotesHonors.objects.get(pk=kp)
        if user != post.editor:
            return render(request, 'quotes/exception/exception_change.html')

        context = {
            'post': post
        }

        return render(request, self.template_name, context)


class DeleteQuotes(ChangeQuotes, DeleteView):
    template_name = 'quotes/users_quotes/delete_quotes.html'

    def get_object(self):
        kp = self.kwargs.get('id')
        return get_object_or_404(QuotesHonors, pk=kp)

    def get_success_url(self) -> str:
        return reverse_lazy('love:home_urls')


class UpdateQuotes(UpdateView):
    template_name = 'quotes/users_quotes/update_quotes.html'
    form_class = QuotesModelForm

    def get(self, request, *args, **kwargs):
        user = Profile.objects.get(user=request.user)
        kp = self.kwargs.get('id')
        post = QuotesHonors.objects.get(pk=kp)
        if user != post.editor:
            return render(request, 'quotes/exception/exception_update.html')

        return super().get(request, *args, **kwargs)

    def get_object(self):
        kp = self.kwargs.get('id')
        return get_object_or_404(QuotesHonors, pk=kp)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('love:change_quotes_urls', kwargs={'id': self.kwargs.get('id')})
