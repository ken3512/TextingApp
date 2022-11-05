from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    title = models.CharField(max_length=20)
    participants = models.ManyToManyField(User, related_name='chats')
    date_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

class Relationship(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to')
    pending = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
