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
from .serializers import ChatSerializer, MessageSerializer, RelationshipSerializer, UserSerializer 
from .models import Chat, Message, Relationship
from django.contrib.auth.models import User
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
        querysetUsers = User.objects.filter(chats__id=chat_id)
        querysetMessages = Message.objects.filter(chat=chat_id)
        users = UserSerializer(querysetUsers, many=True)
        messages = MessageSerializer(querysetMessages, many=True)
        json_data = JSONRenderer().render({"messages": messages.data, "users": users.data})
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
            required=["user_to", "user_from"],
            properties={
                "user_to": openapi.Schema(
                    title="user_to",
                    type=openapi.TYPE_INTEGER,
                ),
                "user_from": openapi.Schema(
                    title="user_from",
                    type=openapi.TYPE_INTEGER,
                ),
            },
        ),
    )
    def post(self, request):
        user_to = request.data["user_to"]
        user_from = request.data["user_from"]
        relationship = Relationship.objects.filter(user_to=user_to, user_from=user_from)
        print(relationship)
        return HttpResponse(status=201)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_to", "user_from"],
            properties={
                "user_to": openapi.Schema(
                    title="user_to",
                    type=openapi.TYPE_INTEGER,
                ),
                "user_from": openapi.Schema(
                    title="user_from",
                    type=openapi.TYPE_INTEGER,
                ),
            },
        ),
    )
    def delete(self, request):
        print(request.DELETE["user_from"])
        # user_to = request.data["user_to"]
        # user_from = request.data["user_from"]
        # relationship = Relationship.objects.filter(user_to=user_to, user_from=user_from).delete()
        return HttpResponse(status=201)


@permission_classes([AllowAny])
class UsersAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
             openapi.Parameter('id', openapi.IN_QUERY, description="", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):
        user_id = request.query_params['id']
        querysetUsers = User.objects.filter(is_active=True).exclude(id=user_id).exclude(user_from__user_to__id=user_id).exclude(user_to__user_from__id=user_id)
        users = UserSerializer(querysetUsers, many=True)
        json_data = JSONRenderer().render(users.data)
        return HttpResponse(json_data, status=201)

@permission_classes([AllowAny])
class FriendsAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
             openapi.Parameter('id', openapi.IN_QUERY, description="", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):
        user_id = request.query_params['id']
        query1 = User.objects.filter(is_active=True, user_to__user_from__id=user_id, user_to__pending=False).exclude(id=user_id)
        query2 = User.objects.filter(is_active=True, user_from__user_to__id=user_id, user_from__pending=False).exclude(id=user_id)
        querysetUsers = (query1 | query2).distinct()
        users = UserSerializer(querysetUsers, many=True)
        json_data = JSONRenderer().render(users.data)
        return HttpResponse(json_data, status=201)

@permission_classes([AllowAny])
class PendingRequestAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
             openapi.Parameter('id', openapi.IN_QUERY, description="", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):
        user_id = request.query_params['id']
        query = User.objects.filter(is_active=True, user_from__user_to__id=user_id, user_from__pending=True).exclude(id=user_id)
        users = UserSerializer(query, many=True)
        json_data = JSONRenderer().render(users.data)
        return HttpResponse(json_data, status=201)

@permission_classes([AllowAny])
class PendingSentAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
             openapi.Parameter('id', openapi.IN_QUERY, description="", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):
        user_id = request.query_params['id']
        query = User.objects.filter(is_active=True, user_to__user_from__id=user_id, user_to__pending=True).exclude(id=user_id)
        users = UserSerializer(query, many=True)
        json_data = JSONRenderer().render(users.data)
        return HttpResponse(json_data, status=201)