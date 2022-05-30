import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all().order_by("-timestamp").values()
    for post in posts:
        post["user"] = User.objects.get(id=post["user_id"])

    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
def post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("message")

        Post.objects.create(user=request.user, text=text)

        return JsonResponse({"message": "Successfully created post!"}, status=201)

    return JsonResponse({"message": "Invalid request method."}, status=400)


@csrf_exempt
@login_required
def profile(request, username):
    alreadyFollows = Follow.objects.filter(
        user=request.user, follower=User.objects.get(username=username)).exists()

    if request.method == "POST":
        if not alreadyFollows:
            Follow.objects.create(
                user=request.user, follower=User.objects.get(username=username))
        else:
            Follow.objects.filter(
                user=request.user, follower=User.objects.get(username=username)).delete()

    followers = Follow.objects.filter(follower__username=username).count()
    following = Follow.objects.filter(user__username=username).count()
    posts = Post.objects.filter(
        user__username=username).order_by("-timestamp").values()

    return render(request, "network/profile.html", {
        "username": username,
        "followers": followers,
        "following": following,
        "posts": posts,
        "follows": alreadyFollows
    })


@csrf_exempt
@login_required
def following(request):
    following = Follow.objects.filter(user=request.user).values()
    posts = []
    for follow in following:
        posts.append(Post.objects.filter(user=follow["follower_id"]).order_by(
            "-timestamp").values()[0])

    for post in posts:
        post["user"] = User.objects.get(id=post["user_id"])

    return render(request, "network/index.html", {
        "posts": posts
    })
