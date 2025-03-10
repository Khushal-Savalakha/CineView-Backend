from django.urls import path
from . import views

urlpatterns = [
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.success_page, name='success-page'),
    path('cancel/', views.payment_cancel, name='cancel'),
    path('download-ticket/', views.download_ticket, name='download-ticket'),
]
