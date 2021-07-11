from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import User, Listing
from .forms import NewListingForm

from datetime import timedelta


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login")
def new_listing(request):

    if request.method == "POST":
        
        form = request.POST
        
        # Grabbing time information and setting listing end date based on chosen duration
        create_date = timezone.now()
        end_date = create_date + timedelta(days = int(form['duration']))
        
        # Attempt to create new listing
        try:
            listing = Listing(
                user = request.user,
                title = form["title"],
                image = form["image"],
                description = form["description"],
                category = form["category"],
                created = create_date,
                end = end_date,
                duration = form["duration"],
                active = True,
                current_bid = form["current_bid"],
            )

            listing.save()
            return HttpResponseRedirect(reverse("index"))

        except:
            return render(request, "auctions/new.html", {
            "form": form,
            "msg": "Unable to create listing. Please try again."
        })


    return render(request, "auctions/new.html", {
        "form": NewListingForm()
    })

def listing(request, id):
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=id)
    })