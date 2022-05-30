import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    fposts = Post.objects.all()
    fposts = fposts.order_by("-timestamp").all()
    posts = Paginator(fposts, 10)

    page_number = request.GET.get('page')
    page_obj = posts.get_page(page_number)
    return render(request, "network/index.html", {
        'page_obj': page_obj
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

def following(request):
    fposts = Post.objects.all()
    for post in fposts:
        if post.creator not in request.user.following.all():
            fposts = fposts.exclude(id=post.id)
    fposts = fposts.order_by("-timestamp").all()
    posts = Paginator(fposts, 10)

    page_number = request.GET.get('page')
    page_obj = posts.get_page(page_number)
    return render(request, "network/following.html", {
        'page_obj': page_obj
    })

@csrf_exempt
def profile(request, username):
    try:
        profile = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    if request.method == 'PUT':
        data = json.loads(request.body) 
        follow = data.get("follow", "")
        if follow:
            profile.followers.add(request.user)
            request.user.following.add(profile)
        else:
            profile.followers.remove(request.user)
            request.user.following.remove(profile)
        return JsonResponse({"message": "Put successful."}, status=201)
    pposts = Post.objects.filter(creator=profile).all()
    pposts = pposts.order_by("-timestamp").all()
    posts = Paginator(pposts, 10)
    page_number = request.GET.get('page')
    page_obj = posts.get_page(page_number)
    return render(request, "network/profile.html", {
            'page_obj': page_obj,
            "profile": profile
        })

@csrf_exempt
@login_required
def posts(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body) 

    # Get contents of email
    body = data.get("body", "")

    post = Post(
        creator=request.user,
        body=body,
    )
    post.save()
    return JsonResponse({"message": "Post successful."}, status=201)

@csrf_exempt
@login_required
def post_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == 'PUT':
        data = json.loads(request.body) 
        var = data.get("var", "")
        if var == 'like':
            post.likes.add(request.user)
            return JsonResponse({"message": "Like successful."}, status=201)
        elif var == 'unlike':
            post.likes.remove(request.user)
            return JsonResponse({"message": "Unlike successful."}, status=201)
        elif var == 'edit':
            post.body = data.get("text", "")
            post.save()
        return JsonResponse({"message": "Edit successful."}, status=201)
    return JsonResponse(post.serialize(), safe=False)

@csrf_exempt
@login_required
def user(request, username):
    user = User.objects.get(username=username)
    return JsonResponse(user.serialize(), safe=False)
 