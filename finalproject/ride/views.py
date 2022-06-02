import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import User

# Create your views here.


def index(request):
    return render(request, 'ride/index.html')


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        user = User(username=username, email=email, password=password)
        user.save()

        return JsonResponse({'status': 'success'}, status=201)

    return render(request, 'ride/register.html')


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email, password=password)
        if user:
            return JsonResponse({'status': 'success'}, status=200)

        return JsonResponse({'status': 'fail'}, status=401)
    return render(request, 'ride/login.html')
