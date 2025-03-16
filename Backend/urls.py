from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # Add this line

def home(request):
    return HttpResponse("Welcome to CineView Backend")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("booking/", include("BookingDetails.urls")),
    path("seats/", include("SeatDetails.urls")),
    path("stripe/", include("stripe_payment.urls")),
    path("", home),
]
