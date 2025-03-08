from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserData
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction

@api_view(['POST'])
def signup(request):
    try:
        with transaction.atomic():
            email = request.data.get('email')
            password = request.data.get('password')
            name = request.data.get('name')

            if not all([email, password, name]):
                return Response({
                    'msg': 'Email, password, and name are required.'
                }, status=status.HTTP_400_BAD_REQUEST)

            if UserData.objects.filter(email=email).exists():
                return Response({
                    'msg': 'Email already registered.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Hash password before saving
            request.data['password'] = make_password(password)
            serializer = UserSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'msg': 'User created successfully!'
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Signup error:", str(e))
        return Response({
            'msg': f'Error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"Login attempt for email: {email}")  # Debug log

        if not all([email, password]):
            return Response({
                'msg': 'Email and password are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserData.objects.get(email=email)
            print(f"User found: {user.name}")  # Debug log
            return Response({
                    'msg': 'Login successful',
                    'user': {
                        'name': user.name,
                        'email': user.email,
                        'data': 'log in Successfully'
                    }
                }, status=status.HTTP_200_OK)
            
            print("Password verification failed")  # Debug log
            return Response({
                'msg': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        except UserData.DoesNotExist:
            print(f"No user found with email: {email}")  # Debug log
            return Response({
                'msg': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug log
        return Response({
            'msg': f'Login failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
