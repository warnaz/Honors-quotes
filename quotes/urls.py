from django.urls import path, include
from .views import (
    create_view,
    QuotesDetail,
    AuthorQuotes, EditorQuotes,
    DeleteQuotes, ChangeQuotes, UpdateQuotes,
    search,
)

from quotes.business.like_comment_logic import (
    
    create_comment,
    create_like,
    create_comment_like,

)

app_name = 'love'

urlpatterns = [
    path('', create_view, name='home_urls'),
    path('comment/', create_comment, name='comment_urls'),
    path('like/', create_like, name='like_urls'),
    path('quote/<int:pk>/', QuotesDetail.as_view(), name='quote_detail_urls'),
    path('comment_like', create_comment_like, name='comment_like_urls'),
    path('author_quotes/<slug:slug>/',
         AuthorQuotes.as_view(), name='author_quotes_urls'),
    path('editor_quotes/<slug:slug>/',
         EditorQuotes.as_view(), name='editor_quotes_urls'),
    path('change_quotes/<int:id>/', ChangeQuotes.as_view(),
         name='change_quotes_urls'),
    path('update_quotes/<int:id>/', UpdateQuotes.as_view(),
         name='update_quotes_urls'),
    path('delete_post/<int:id>/', DeleteQuotes.as_view(), name='delete_post_urls'),
    path('search', search, name='search_urls'),

]
