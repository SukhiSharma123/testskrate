from rest_framework.response import Response
from rest_framework import (
    generics, 
    permissions, 
    status, 
    )
from rest_framework.views import APIView
from .models import *
from .serializers import (
    UserSerializer,
)
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import CharField, Value, IntegerField, Q
User = get_user_model()

class UserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permissions_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'token': token,
        }
        return response

