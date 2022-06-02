import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError

from .models import User

# Create your views here.


def index(request):
    return render(request, 'ride/index.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "ride/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "ride/register.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect("/login")
    else:
        return render(request, "ride/register.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/rides")
        else:
            return render(request, "ride/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "ride/login.html")


def rides(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    return render(request, 'ride/ride.html')
