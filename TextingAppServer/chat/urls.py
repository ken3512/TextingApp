from django.urls import path
from .views import MessageAIPView, ChatAPIView, AddUserAPIView, RelationshipAPIView, AddBackAPIView, UsersAPIView


urlpatterns = [
    path('message/', MessageAIPView.as_view()),
    path('chat/', ChatAPIView.as_view()),
    path('add/', AddUserAPIView.as_view()),
    path('friend/', RelationshipAPIView.as_view()),
    path('all/', UsersAPIView.as_view()),
    path('confirm/', AddBackAPIView.as_view()),
]