from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserData
from .serializers import UserSerializer
from django.db import transaction
from django.contrib.auth.hashers import check_password


@api_view(["POST"])
def signup(request):
    try:
        with transaction.atomic():
            email = request.data.get("email")
            password = request.data.get("password")
            name = request.data.get("name")

            if not all([email, password, name]):
                return Response(
                    {"msg": "Email, password, and name are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if UserData.objects.filter(email=email).exists():
                return Response(
                    {"msg": "Email already registered."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Simply pass the data directly without hashing
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "User created successfully!"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {"msg": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"msg": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = UserData.objects.get(email=email)

        # Use check_password to verify hashed password
        if check_password(password, user.password):
            serializer = UserSerializer(user)
            return Response(
                {"msg": "Login successful", "user": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"msg": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
        )

    except UserData.DoesNotExist:
        return Response({"msg": "User not found."}, status=status.HTTP_404_NOT_FOUND)
