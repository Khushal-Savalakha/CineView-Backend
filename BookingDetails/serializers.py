from .models import BookingData
from rest_framework import serializers


class BookingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingData
        fields = ["email", "movie_name", "date", "time_slot", "seat_number", "amount"]
