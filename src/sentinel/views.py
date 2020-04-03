from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import RedirectView


def home(request):
    return redirect("admin/")
