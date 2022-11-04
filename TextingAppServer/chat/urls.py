from django.urls import path
from .views import MessageAIPView, ChatAPIView


urlpatterns = [
    path('message/', MessageAIPView.as_view()),
    path('chat/', ChatAPIView.as_view()),
]