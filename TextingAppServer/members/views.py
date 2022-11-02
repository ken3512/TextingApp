from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
@swagger_auto_schema()
def login_user(request):
    if request.method != "POST":
        return JsonResponse({'data': NULL, 'error': 'method not post'})
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        data = login(request, user)
        return JsonResponse({'data': data, 'error': ''})
    else:
        return JsonResponse({'data': NULL, 'error': 'User not valid'})
    
@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
@swagger_auto_schema()
def logout_user(request):
    logout(request)
    return JsonResponse({'data': NULL, 'error': ''})
