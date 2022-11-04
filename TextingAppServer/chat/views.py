from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from drf_yasg import openapi
from .serializers import ChatSerializer, MessageSerializer

class MessageAIPView(APIView):

    @swagger_auto_schema(
        request_body=MessageSerializer,
    )
    def post(self, request):
        pass

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
             openapi.Parameter('chat_id', openapi.IN_PATH, description="", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):
        pass