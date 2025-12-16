from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer
from .models import User


@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"})
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": UserSerializer(user).data
    })


@api_view(["GET"])
def me(request):
    return Response(UserSerializer(request.user).data)



@api_view(["POST"])
def refresh_token(request):
    refresh_token = request.data.get("refresh")
    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return Response({"access": access_token})
    except Exception as e:
        return Response({"error": "Invalid refresh token"}, status=400)


