from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import RedirectView
# from django.contrib.auth import
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.conf import settings
from django.views.generic import View

class DashboardLogin(View):
    def get(self,request):
        return HttpResponseRedirect(reverse("django_auth_adfs:login"))

    def post(self,request):
        return HttpResponseRedirect(reverse("django_auth_adfs:login"))

class DashboardLogout(View):
    def get(self,request):
        return HttpResponseRedirect(reverse("django_auth_adfs:logout"))

    def post(self,request):
        return HttpResponseRedirect(reverse("django_auth_adfs:logout"))

def home(request):
    if request.user.is_active:
        if request.user.is_authenticated:
            print(request.user)
            return redirect("admin/")
        else:
            return redirect("/oauth2/login")
    else:
        return redirect("/oauth2/login")

def login_redirect(request):
    return HttpResponseRedirect(reverse("django_auth_adfs:login"))

def logout_redirect(request):
    # return HttpResponseRedirect(reverse("/ouath2/logout/"))
    return redirect("/ouath2/logout/")
