from rest_framework import serializers
from .models import MovieAvailability

class MovieAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieAvailability
        fields = ['movie_name', 'date', 'time_slot', 'seat_status']
        
    def validate(self, data):
        if not all(key in data for key in ['movie_name', 'date', 'time_slot']):
            raise serializers.ValidationError("Missing required fields")
        return data