from django.urls import path, include
from .views import (
    UpProf,
    users_view,
    UsersClass,

)
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'profile'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('upprof/<slug:slug>', UpProf.as_view(), name='upprof_urls'),
    path('users/', users_view, name='users_urls'),
    path('<slug:slug>/', UsersClass.as_view(), name='users_detail_urls'),
]
    
