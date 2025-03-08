from django.db import models


class UserData(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.TextField()

    class Meta:
        db_table = "api_userdata"

    def __str__(self):
        return f"{self.name} ({self.email})"
