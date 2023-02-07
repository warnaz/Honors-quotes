from django import template
from quotes.models import *
from author.models import *
from django.db.models import Prefetch
from django.db.models import Count, Q
from django.core.paginator import Paginator

register = template.Library()


@register.inclusion_tag('quotes/list_quotes.html')
def show_quotes(request, name, slug=None):
    user = Profile.objects.get(user=request.user)

    if name == 'quotes':
        qs = get_qs()
        return {"qs": qs, 'user': user}

    elif name == 'author':
        qs = get_qs().filter(author=slug)
        if qs:
            return {"qs": qs, 'user': user}

    elif name == 'editor':
        qs = get_qs().filter(editor=slug)
        if qs:
            return {"qs": qs, 'user': user}

    elif name == 'search':
        search = request.GET.get('q', '')
        if search:
            qs = get_qs().filter(
                Q(quotes__icontains=search) | Q(author__user__username=search) |
                Q(author__first_name__icontains=search) | Q(author__last_name__icontains=search))

            return {"qs": qs, 'user': user}


def get_qs():
    return QuotesHonors.objects.prefetch_related('quotes_comment').select_related(
        'author', 'editor').prefetch_related('liked', 'category')
