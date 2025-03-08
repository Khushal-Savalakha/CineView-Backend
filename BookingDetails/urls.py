# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.insert_booking_data, name="insert_booking_data"),
    path("search/", views.search_booking_data, name="search_booking_data"),
    path("get-csrf-token/", views.get_csrf_token, name="get_csrf_token"),
]
