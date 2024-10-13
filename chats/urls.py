from .views import chats
from django.urls import path
urlpatterns = [
    path('', chats, name='chats'),
    path('mychats/', chats, name='mychats'),
]