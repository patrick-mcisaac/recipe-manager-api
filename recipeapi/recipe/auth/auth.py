from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):

    username = request.data.get("username")
    password = request.data.get("password")

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)

        data = {"valid": True, "token": token.key}
        return Response(data)
    else:
        data = {"valid": False}
        return Response(data)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    email = request.data.get("email", None)
    username = request.data.get("username", None)
    first_name = request.data.get("first_name", None)
    last_name = request.data.get("last_name", None)
    password = request.data.get("password", None)

    if (
        email is not None
        and first_name is not None
        and last_name is not None
        and username is not None
        and password is not None
    ):
        try:
            new_user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
        except IntegrityError:
            return Response(
                {"message": "An account with that username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = Token.objects.create(user=new_user)
        data = {"token": token.key}
        return Response(data)

    return Response(
        {"message": "You must provide email, password, first_name, and last_name"},
        status=status.HTTP_400_BAD_REQUEST,
    )
