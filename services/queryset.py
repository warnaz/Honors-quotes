from quotes.models import QuotesHonors
from author.models import Profile
from . import decorators

def get_profile(user):
    return Profile.objects.get(user=user)

def all_profile():
    return Profile.objects.all()

def filter_profile(*args, **kwargs):
    return Profile.objects.filter(*args, **kwargs)


def get_quotes(quotes):
    return QuotesHonors.objects.prefetch_related('quotes_comment').select_related(
        'author', 'editor').prefetch_related('liked', 'category').get()

def all_quotes():
    return get_quotes()

@decorators.filter_decorator_quotes
def filter_quotes(*args, **kwargs):
    return Profile.objects.filter(*args, **kwargs)



