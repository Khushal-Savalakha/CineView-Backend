from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('signup/', csrf_exempt(views.signup), name='user-signup'),
    path('login/', csrf_exempt(views.login), name='user-login'),
]
