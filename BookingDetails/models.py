from django.db import models

# Create your models here.
class BookingData(models.Model):
    email= models.EmailField()
    movie_name = models.CharField(max_length=255)
    date = models.CharField(max_length=50)
    time_slot = models.CharField(max_length=50)
    seat_number=models.CharField(max_length=255)
    amount=models.IntegerField()