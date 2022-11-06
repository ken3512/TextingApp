from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .serializers import ChatSerializer, MessageSerializer, RelationshipSerializer
from .models import Chat, Message, Relationship
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
        return HttpResponse(json_data, status=201)

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
        return HttpResponse(json_data, status=201)

@permission_classes([AllowAny])
class AddUserAPIView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["chat_id", "user_id"],
            properties={
                "chat_id": openapi.Schema(
                    title="Chat_id",
                    type=openapi.TYPE_INTEGER,
                ),
                "user_id": openapi.Schema(
                    title="User_id",
                    type=openapi.TYPE_INTEGER,
                ),
            },
        ),
    )
    def post(self, request):
        chat_id = request.data["chat_id"]
        user_id = request.data["user_id"]
        chat = Chat.objects.get(id=chat_id)
        chat.participants.add(user_id)
        chat.save()
        return HttpResponse(status=201)



@permission_classes([AllowAny])
class RelationshipAPIView(APIView):

    @swagger_auto_schema(
        request_body=RelationshipSerializer,
    )
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = RelationshipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @swagger_auto_schema(
        manual_parameters=[
             openapi.Parameter('user_to', openapi.IN_QUERY, description="", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):
        user_to = request.query_params['user_to']
        queryset = Relationship.objects.filter(user_to=user_to)
        relationships = RelationshipSerializer(queryset, many=True)
        json_data = JSONRenderer().render(relationships.data)
        return HttpResponse(json_data, status=201)

@permission_classes([AllowAny])
class AddBackAPIView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["relationship_id"],
            properties={
                "relationship_id": openapi.Schema(
                    title="relationship_id",
                    type=openapi.TYPE_INTEGER,
                ),
            },
        ),
    )
    def post(self, request):
        relationship_id = request.data["relationship_id"]
        relationship = Relationship.objects.get(id=relationship_id)
        relationship.pending = False
        relationship.save()
        return HttpResponse(status=201)