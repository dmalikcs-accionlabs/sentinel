__author__ = "Rasmita Sahoo"
from .views import ReadEmailView, ExecuteParserView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    path('read/<uuid:token>/', csrf_exempt(ReadEmailView.as_view()), name="read_email"),
    path('parser/<uuid:pk>/execute/', csrf_exempt(ExecuteParserView.as_view()), name="execute_parser"),
    ]