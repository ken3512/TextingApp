from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .serializers import ChatSerializer, MessageSerializer
from .models import Chat, Message
import datetime

@permission_classes([AllowAny])
class MessageAIPView(APIView):

    @swagger_auto_schema(
        request_body=MessageSerializer,
    )
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            chat_id = serializer.data.get("chat")
            chat = Chat.objects.get(id=chat_id)
            chat.date_modified = datetime.datetime.now()
            chat.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @swagger_auto_schema(
        manual_parameters=[
             openapi.Parameter('chat_id', openapi.IN_QUERY, description="", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):
        chat_id = request.query_params['chat_id']
        queryset = Message.objects.filter(chat=chat_id)
        messages = MessageSerializer(queryset, many=True)
        json_data = JSONRenderer().render(messages.data)
        return HttpResponse(json_data)

@permission_classes([AllowAny])
class ChatAPIView(APIView):

    @swagger_auto_schema(
        request_body=ChatSerializer,
    )
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ChatSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @swagger_auto_schema(
        manual_parameters=[
             openapi.Parameter('user_id', openapi.IN_QUERY, description="", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):
        user_id = request.query_params['user_id']
        queryset = Chat.objects.filter(participants=user_id).order_by('-date_modified')
        chats = ChatSerializer(queryset, many=True)
        json_data = JSONRenderer().render(chats.data)
        return HttpResponse(json_data)