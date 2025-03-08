from django.contrib import admin
from .models import BookingData
# Register your models here.

@admin.register(BookingData)
class BookingDataSerializer(admin.ModelAdmin):
    list_display=['id','email','movie_name','date','time_slot','seat_number','amount']