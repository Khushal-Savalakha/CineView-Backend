from django.urls import path
from SeatDetails import views

urlpatterns = [
    # URL pattern for checking seat availability by movie_name, date, and time_slot
    path("seatsdata/", views.seats_data, name="seats_data"),
    # URL pattern for updating the availability of a particular movie slot
    path("updateseat/", views.update_seat, name="update_seat"),
    # URL pattern for adding new movie availability data
    path("addseats/", views.add_seats_data, name="add_seats_data"),
    path("get-csrf-token/", views.get_csrf_token, name="get_csrf_token"),
]
