from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'ride/index.html')


def register(request):
    return render(request, 'ride/register.html')


def login(request):
    return render(request, 'ride/login.html')
