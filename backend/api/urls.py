from django.contrib.auth import views as auth
from django.contrib.auth.views import logout_then_login
from django.urls import re_path, reverse_lazy, path
from django.views.generic import RedirectView


from . import views as api

urlpatterns = [
    path('messages', api.message_view, name="messages"),
]