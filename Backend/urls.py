from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("booking/", include("BookingDetails.urls")),
    path("seats/", include("SeatDetails.urls")),
    path("stripe/", include("stripe_payment.urls")),  # Add this line
]
