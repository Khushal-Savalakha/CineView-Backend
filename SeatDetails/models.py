from django.db import models

class MovieAvailability(models.Model):
    movie_name = models.CharField(max_length=255)
    date = models.CharField(max_length=30)
    time_slot = models.CharField(max_length=20)
    seat_status = models.CharField(
        max_length=100, 
        default='1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1'
    )

    class Meta:
        unique_together = ('movie_name', 'date', 'time_slot')
        
    def __str__(self):
        return f"{self.movie_name} - {self.date} - {self.time_slot}"

