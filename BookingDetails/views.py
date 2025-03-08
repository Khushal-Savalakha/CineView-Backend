from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import BookingData
from .serializers import BookingDataSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
def insert_booking_data(request):
    # Insert new booking data
    serializer = BookingDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def search_booking_data(request):
    print("Received search request:", request.data)  # Debug log
    try:
        email = request.data.get('email')
        print(f"Searching bookings for email: {email}")  # Debug log
        
        if not email:
            return Response({
                'error': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        bookings = BookingData.objects.filter(email=email)
        print(f"Found {bookings.count()} bookings")  # Debug log
        
        if not bookings.exists():
            return Response({
                'message': 'No bookings found for this email',
                'data': []
            }, status=status.HTTP_200_OK)  # Changed from 404 to 200

        serializer = BookingDataSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Error in search_booking_data: {str(e)}")  # Debug log
        return Response({
            'error': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_csrf_token(request):
    return Response({'csrfToken': get_token(request)})
