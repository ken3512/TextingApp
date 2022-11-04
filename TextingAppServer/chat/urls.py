from django.urls import path
from .views import MessageAIPView, ChatAPIView, AddUserAPIView


urlpatterns = [
    path('message/', MessageAIPView.as_view()),
    path('chat/', ChatAPIView.as_view()),
    path('add/', AddUserAPIView.as_view()),
]