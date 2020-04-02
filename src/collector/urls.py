__author__ = "Rasmita Sahoo"
from django.urls import path
from .views import ReadEmailView,TestReadEmail
urlpatterns = [

    path('read/', ReadEmailView.as_view(
    ), name="read_email"),
    path('r/', TestReadEmail.as_view(
    ), name="read"),
    ]