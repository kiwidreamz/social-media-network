from cgi import print_environ
from datetime import date, datetime
from multiprocessing import context
from urllib import request
from xmlrpc.client import DateTime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import datetime
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Posts, Following, Likez


def index(request):

    current_user = request.user
    current_page = 1
    next_page = 2

    # Get all posts
    posts = Posts.objects.all().order_by('-dateandtime')

    if len(posts) > 10:
        first_page = True
    else:
        first_page = False

    # Pagination
    p = Paginator(posts, 10)
    posts = p.page(1)

    likez = Likez.objects.all

    context = {
        "posts": posts,
        "current_user": current_user,
        "current_page": current_page,
        "first_page": first_page,
        "next_page": next_page,
        "last_page": False,
        "likez": likez,
    }

    return render(request, "network/index.html", context)

def page(request, page_num):

    next_page = page_num + 1
    previous_page = page_num - 1
    current_user = request.user

    # Get all posts
    all_posts = Posts.objects.all().order_by('-dateandtime')

    # Pagination
    p = Paginator(all_posts, 10)
    number_of_pages = p.num_pages

    # If no pagination number received, output first page
    if not page_num:
        posts = p.page(1)
    else:
        posts = p.page(page_num)

    # Check if first page
    if page_num == 1:
        first_page = True
    else:
        first_page = False

    # Check if last page
    if page_num >= number_of_pages:
        last_page = True
    else:
        last_page = False

    context = {
        "posts": posts,
        "current_user": current_user,
        "last_page": last_page,
        "first_page": first_page,
        "p": p,
        "current_page": page_num,
        "next_page": next_page,
        "previous_page": previous_page,
    }

    return render(request, "network/index.html", context)


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

@login_required
def submit(request):
    
    newpost_text = request.POST["newpost_text"]

    if len(newpost_text) > 0:
        pass
    else:
        return render(request, "network/error.html", {
            "message": "Text cannot be empty"
        })

    user = request.user

    # Create new post and save it in the database
    new_post = Posts.objects.create(user = user, dateandtime = datetime.datetime.now(), text = newpost_text, likes = 0)
    new_post.save()

    return HttpResponseRedirect(reverse("index"))


def profile(request, user_id):

    user = User.objects.get(pk=user_id)
    current_user = request.user
    followed = False
    current_page = 1
    next_page = 2

    # Get following and followers counts
    following_count = Following.objects.filter(user=user).count()
    followers_count = Following.objects.filter(following=user).count()

    # Check if followed
    if request.user.is_anonymous:
        followed = False
    elif Following.objects.filter(user = current_user, following = user):
        followed = True
    else:
        followed = False

    posts = Posts.objects.filter(user=user).order_by('-dateandtime')

    if len(posts) < 10:
        last_page = True
    else:
        last_page = False

    # Pagination
    p = Paginator(posts, 10)
    posts = p.page(1)

    # Check if own profile
    if user == current_user:
        can_edit = True
    else:
        can_edit = False

    context = {
        "posts": posts,
        "user": user,
        "following_count": following_count,
        "followers_count": followers_count,
        "followed": followed,
        "current_user": current_user,
        "first_page": True,
        "next_page": next_page,
        "last_page": last_page,
        "can_edit": can_edit,
    }


    return render(request, "network/profile.html", context)   


def follow(request, user_to_follow):

    user = request.user
    user_to_follow = User.objects.get(pk=user_to_follow)

    # Create following object and save it
    follow = Following.objects.create(user = user, following = user_to_follow)
    follow.save()

    # Get following and followers counts
    following_count = Following.objects.filter(user=user_to_follow).count()
    followers_count = Following.objects.filter(following=user_to_follow).count()

    posts = Posts.objects.filter(user=user_to_follow).order_by('-dateandtime')
    followed = False

    # Check if followed
    exists = Following.objects.filter(user = user, following = user_to_follow).exists()
    if exists:
        followed = True
    else:
        followed = False

    context = {
        "posts": posts,
        "user": user_to_follow,
        "following_count": following_count,
        "followers_count": followers_count,
        "followed": followed,
        "current_user": user,
    }

    return render(request, "network/profile.html", context)   

def unfollow(request, user_to_unfollow):

    user = request.user
    user_to_unfollow = User.objects.get(pk=user_to_unfollow)

    # Find following object and delete it
    unfollow = Following.objects.get(user = user, following = user_to_unfollow)
    unfollow.delete()

    # Get following and followers counts
    following_count = Following.objects.filter(user=user_to_unfollow).count()
    followers_count = Following.objects.filter(following=user_to_unfollow).count()

    posts = Posts.objects.filter(user=user_to_unfollow).order_by('-dateandtime')
    followed = False

    # Check if followed
    exists = Following.objects.filter(user = user, following = user_to_unfollow).exists()
    if exists:
        followed = True
    else:
        followed = False

    context = {
        "posts": posts,
        "user": user_to_unfollow,
        "following_count": following_count,
        "followers_count": followers_count,
        "followed": followed,
        "current_user": user,
    }

    return render(request, "network/profile.html", context)   


@login_required
def following(request):

    current_user = request.user
    following_array = Following.objects.filter(user_id = current_user)
    next_page = 2
    
    # Declare list variables
    posts_list = list()
    posts = list()

    # Create a 2d array with posts from followed users
    for instance in following_array:
        id = instance.following_id
        posts_list.append(Posts.objects.filter(user_id = id).order_by('-dateandtime'))

    # Flatten 2d array
    posts = [post for sublist in posts_list for post in sublist]

    if len(posts) < 10:
        last_page = True
    else:
        last_page = False

    # Pagination
    p = Paginator(posts, 10)
    posts = p.page(1)

    context = {
        "posts": posts,
        "current_user": current_user,
        "first_page": True,
        "next_page": next_page,
        "last_page": last_page,
    }

    return render(request, "network/following.html", context)


def profile_page(request, user_id, profile_page):

    user = User.objects.get(pk=user_id)
    current_user = request.user
    followed = False
    next_page = profile_page + 1
    previous_page = profile_page - 1

    # Get following and followers counts
    following_count = Following.objects.filter(user=user).count()
    followers_count = Following.objects.filter(following=user).count()

    # Check if followed
    if Following.objects.filter(user = current_user, following = user):
        followed = True
    else:
        followed = False

    posts = Posts.objects.filter(user=user).order_by('-dateandtime')
    print(len(posts))

    # Pagination
    p = Paginator(posts, 10)
    posts = p.page(1)
    number_of_pages = p.num_pages

    # Check if first or last page
    if profile_page == 1:
        first_page = True
    else:
        first_page = False

    if profile_page >= number_of_pages:
        last_page = True
    else:
        last_page = False

    # If no pagination number received, output first page
    if not profile_page:
        posts = p.page(1)
    else:
        posts = p.page(profile_page)

    # Check if own profile
    if user == current_user:
        can_edit = True
    else:
        can_edit = False

    context = {
        "posts": posts,
        "user": user,
        "following_count": following_count,
        "followers_count": followers_count,
        "followed": followed,
        "current_user": current_user,
        "first_page": first_page,
        "last_page": last_page,
        "previous_page": previous_page,
        "next_page": next_page,
        "can_edit": can_edit,
    }

    return render(request, "network/profile.html", context)

def following_page(request, following_page):

    current_user = request.user
    following_array = Following.objects.filter(user_id = current_user)
    next_page = following_page + 1
    previous_page = int(following_page) - 1
    
    # Declare list variables
    posts_list = list()
    posts = list()

    # Create a 2d array with posts from followed users
    for instance in following_array:
        id = instance.following_id
        posts_list.append(Posts.objects.filter(user_id = id).order_by('-dateandtime'))

    # Flatten 2d array
    posts = [post for sublist in posts_list for post in sublist]

    # Pagination
    p = Paginator(posts, 10)
    number_of_pages = p.num_pages

    # Check if first or last page
    if following_page == 1:
        first_page = True
    else:
        first_page = False

    if following_page >= number_of_pages:
        last_page = True
    else:
        last_page = False

    # If no pagination number received, output first page
    if not following_page:
        posts = p.page(1)
    else:
        posts = p.page(following_page)

    context = {
        "posts": posts,
        "current_user": current_user,
        "first_page": first_page,
        "last_page": last_page,
        "previous_page": previous_page,
        "next_page": next_page,
    }

    return render(request, "network/following.html", context)

@csrf_exempt
def edit(request, post_id):

    if request.method == "POST":
        post = Posts.objects.get(id=post_id)
        textarea = request.POST["textarea"]
        post.text = textarea
        post.save()

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    if request.method == "PUT":
        post = Posts.objects.get(id=post_id)
        data = json.loads(request.body)

        print(data)

        post.text = data
        post.save()
        return JsonResponse({"post": post.text})


@csrf_exempt
def like(request, post_id):
    post = Posts.objects.get(id=post_id)

    if request.method == "GET":
        return HttpResponseRedirect(reverse("index"))
    
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like"):
            Likez.objects.create(user = request.user, post = post)
            post.likes = Likez.objects.filter(post = post).count()
        else:
            Likez.objects.filter(user = request.user, post = post).delete()
            post.likes = Likez.objects.filter(post_id = post).count()
        post.save()

    return JsonResponse({"likes": post.likes})

    
