from django.urls import path
from .views import *

urlpatterns = [
    path('login_user', login_user)
]
