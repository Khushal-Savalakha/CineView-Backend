from django.contrib import admin
from .models import MovieAvailability

@admin.register(MovieAvailability)
class MovieAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie_name', 'date', 'time_slot', 'seat_status']
