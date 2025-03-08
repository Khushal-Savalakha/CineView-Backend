from rest_framework import status
from rest_framework.response import Response
from .models import MovieAvailability
from .serializers import MovieAvailabilitySerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token


@csrf_exempt
@api_view(["POST"])
def add_seats_data(request):
    try:
        movie_name = request.data.get("movie_name")
        date = request.data.get("date")
        time_slot = request.data.get("time_slot")
        seat_status = request.data.get(
            "seat_status", "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
        )

        # Check if record already exists
        existing_record = MovieAvailability.objects.filter(
            movie_name=movie_name, date=date, time_slot=time_slot
        ).first()

        if existing_record:
            return Response(
                {"error": "Movie availability already exists for this slot"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create new record
        movie_availability = MovieAvailability.objects.create(
            movie_name=movie_name,
            date=date,
            time_slot=time_slot,
            seat_status=seat_status,
        )

        serializer = MovieAvailabilitySerializer(movie_availability)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": f"Failed to add seats: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def seats_data(request):
    movie_name = request.data.get("movie_name")
    date = request.data.get("date")
    time_slot = request.data.get("time_slot")

    if not all([movie_name, date, time_slot]):
        return Response(
            {"error": "movie_name, date, and time_slot are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        availability = MovieAvailability.objects.filter(
            movie_name=movie_name, date=date, time_slot=time_slot
        ).first()

        if availability:
            serializer = MovieAvailabilitySerializer(availability)
            return Response(serializer.data)

        # Create new availability if it doesn't exist
        new_availability = MovieAvailability.objects.create(
            movie_name=movie_name,
            date=date,
            time_slot=time_slot,
            seat_status="1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
        )
        serializer = MovieAvailabilitySerializer(new_availability)
        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
def update_seat(request):
    """
    Update or create availability for a particular movie slot.
    Requires movie_name, date, time_slot, and availability data.
    """

    try:
        movie_name = request.data.get("movie_name")
        date = request.data.get("date")
        time_slot = request.data.get("time_slot")
        seat_status = request.data.get("seat_status")

        # Check if the record exists
        slot, created = MovieAvailability.objects.update_or_create(
            movie_name=movie_name,
            date=date,
            time_slot=time_slot,
            defaults={"seat_status": seat_status},
        )

        if created:
            return Response(
                {"msg": "Booking created successfully."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"msg": "Booking updated successfully."}, status=status.HTTP_200_OK
            )

    except Exception as e:
        return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def get_csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})
