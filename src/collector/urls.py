__author__ = "Rasmita Sahoo"
from .views import ReadEmailView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    path('read/', csrf_exempt(ReadEmailView.as_view()), name="read_email"),
    ]