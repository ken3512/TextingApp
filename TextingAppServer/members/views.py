from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_user(request):
    if request.method != "POST":
        return JsonResponse({'error': 'method not post'})
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'error': ''})
    else:
        return JsonResponse({'error': 'User not valid'})
    

def logout_user(request):
    logout(request)
    return JsonResponse({'error': ''})
