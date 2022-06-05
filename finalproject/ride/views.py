import json
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError

from .models import User, Ride, Message

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/rides')

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
        if request.user.is_authenticated:
            return HttpResponseRedirect("/rides")

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
        if request.user.is_authenticated:
            return HttpResponseRedirect("/rides")

        return render(request, "ride/login.html")


def rides(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    return render(request, 'ride/ride.html')


def new_ride(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == "POST":
        departure = request.POST["departure"]
        destination = request.POST["destination"]
        schedule = request.POST["schedule"]
        seats = request.POST["seats"]
        price = request.POST["price"]

        user = request.user

        ride = Ride.objects.create(
            departure=departure,
            destination=destination,
            schedule=schedule,
            seats=seats,
            price=price,
            driver=user
        )

        ride.save()

        return HttpResponseRedirect("/rides")

    return render(request, 'ride/new_ride.html')


def get_rides(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    rides = Ride.objects.all()
    rides_list = []

    for ride in rides:
        rides_list.append({
            "id": ride.id,
            "departure": ride.departure,
            "destination": ride.destination,
            "schedule": ride.schedule,
            "seats": ride.seats,
            "price": ride.price,
            "driver": ride.driver.username,
            "passengers": [passenger.username for passenger in ride.passengers.all()],
            "available": True if ride.driver != request.user else False
        })

    return JsonResponse(rides_list, safe=False)


def personal_rides(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    rides = Ride.objects.filter(driver=request.user)
    rides_list = []

    for ride in rides:
        rides_list.append({
            "id": ride.id,
            "departure": ride.departure,
            "destination": ride.destination,
            "schedule": ride.schedule,
            "seats": ride.seats,
            "price": ride.price,
            "driver": ride.driver.username,
            "passengers": [passenger.username for passenger in ride.passengers.all()]
        })

    accepted = Ride.objects.filter(passengers=request.user)
    accepted_list = []

    for ride in accepted:
        accepted_list.append({
            "id": ride.id,
            "departure": ride.departure,
            "destination": ride.destination,
            "schedule": ride.schedule,
            "seats": ride.seats,
            "price": ride.price,
            "driver": ride.driver.username,
            "passengers": [passenger.username for passenger in ride.passengers.all()]
        })

    return render(request, 'ride/personal_rides.html', {
        "rides": rides_list,
        "accepted": accepted_list
    })


def delete_ride(request, ride_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    ride = Ride.objects.get(id=ride_id)
    if ride.driver != request.user:
        return HttpResponseRedirect('/rides')
    ride.delete()

    return HttpResponseRedirect("/rides/personal")


def ride_details(request, ride_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    ride = Ride.objects.get(id=ride_id)
    passengers = [passenger.username for passenger in ride.passengers.all()]

    messages = Message.objects.filter(ride=ride)
    interested = ride.interested.all()
    confirmed = ride.passengers.all()

    return render(request, 'ride/ride_details.html', {
        "ride": ride,
        "passengers": passengers,
        "messages": messages,
        "interested": interested,
        "confirmed": confirmed
    })


@csrf_exempt
def message_ride(request, ride_id):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data["message"]
        ride = Ride.objects.get(id=ride_id)
        user = request.user

        message = Message.objects.create(
            message=message,
            ride=ride,
            sender=user,
            receiver=ride.driver
        )

        message.save()

        return HttpResponseRedirect(f"/ride/{ride_id}")


def interested(request, ride_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    ride = Ride.objects.get(id=ride_id)
    user = request.user

    if not user in ride.interested.all():
        ride.interested.add(user)

    else:
        ride.interested.remove(user)
    ride.save()

    return redirect(f"/ride/{ride_id}")


def confirm_passenger(request, ride_id, user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    ride = Ride.objects.get(id=ride_id)
    user = User.objects.get(id=user_id)

    if request.user == ride.driver and user in ride.interested.all():
        ride.passengers.add(user)
        ride.interested.remove(user)
        ride.seats -= 1
        ride.save()

    elif request.user == ride.driver and user in ride.passengers.all():
        ride.passengers.remove(user)
        ride.seats += 1
        ride.save()

    elif request.user == user:
        ride.passengers.remove(user)
        ride.seats += 1
        ride.save()

    return redirect(f"/ride/{ride_id}")
