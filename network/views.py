from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.urls import reverse
import datetime
from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, UserFollowing


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.all().order_by("-date"),
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


def create_post(request):
    if request.method == "POST":
        body = request.POST['body']
        date = datetime.datetime.now()
        new_user = Post(body=body, date=date, user=request.user)
        new_user.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "network/create_post.html")


# @login_required(login_url='login')
@csrf_exempt
def like(request):
    if request.method != 'PUT':
        return JsonResponse({"error": "PUT request required."}, status=400)
        # Ensure the CSRF token is included in the response
    data = json.loads(request.body)
    print("Data received:", data)
    post = Post.objects.get(pk=data["postId"])
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return JsonResponse({"amount_of_likes": post.likes.count()}, status=200)


@csrf_exempt
def edit_post(request):
    if request.method!="PUT":
        return JsonResponse({"error": "PUT request required."},status=400)
    data=json.loads(request.body)
    # safe method
    post_id = data.get("post_id")
    new_body = data.get("new_body")
    if post_id is None or new_body is None:
        return JsonResponse({"error": "Missing required parameters."}, status=400)

    try:
        post=Post.objects.get(pk=post_id)
        if post.user == request.user:

            post.body=new_body
            post.save()
            return JsonResponse({"message": "Successfully updated body of the post."},status=200)
        else:
            return JsonResponse({"error": "You are not the author of this post. Go Away!"},status=403)
    except ObjectDoesNotExist:
        return JsonResponse({"error": f"Post with ID {post_id} does not exist."},status=404)

def profile(request, profile_id):
    person = User.objects.get(pk=profile_id)
    follower = False
    if request.user.is_authenticated:
        try:
            follow_data = UserFollowing.objects.get(user_id=request.user, following_user_id=profile_id)

            if follow_data != None:
                follower = follow_data
                # print(follow_data.created)


        except ObjectDoesNotExist:
            pass
    return render(request, "network/profile.html", {
        "person": person,
        "follower": follower,
    })

@login_required(login_url="login")
def follow(request,profile_id,special_key):
    """
    except ObjectDoesNotExist:
    I can do instead of special_keys.
    But it works fine though
    """
    if special_key == 1:
        # unfollow from this user
        print(f"unfollow from {profile_id}")
        follow_data=UserFollowing.objects.get(user_id=request.user, following_user_id=profile_id)
        follow_data.delete()
        print(f"Following after: {request.user.following.all()}")
    elif special_key == 2:
        #follow
        print(f"follow to {profile_id}")
        famous_user=User.objects.get(pk=profile_id)
        new_follow_data=UserFollowing(user_id=request.user,following_user_id=famous_user)
        new_follow_data.save()
    return HttpResponseRedirect(reverse("profile",args=(profile_id,)))

@login_required(login_url="login")
def following(request):
    following = request.user.following.all()
    following_people = [each.following_user_id for each in following]
    print(following_people)
    post_from_following=Post.objects.filter(user__in=following_people).order_by("-date")

    return render(request,"network/new_following.html", {
        "posts": post_from_following,
    })