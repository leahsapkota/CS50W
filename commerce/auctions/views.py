from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": allCategories,
    })


def displayCategory(request):
    if request.method=="POST":
        if 'category' in request.POST:
            categoryFromForm = request.POST['category']
            category = Category.objects.get(categoryName=categoryFromForm)
            activeListings = Listing.objects.filter(isActive=True, category=category)
            allCategories = Category.objects.all()
            return render(request, "auctions/index.html", {
            "listings": activeListings,
            "categories": allCategories,    
            })


@login_required
def createListing(request):
    
    if request.method =="GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "categories": allCategories
        })  
        
    else: 
        title = request.POST["title"]
        description = request.POST["description"]
        imageUrl = request.POST["imageUrl"]
        price = request.POST["price"]
        category = request.POST.get("category")
        currentUser = request.user
        categoryData = get_object_or_404(Category, categoryName=category)              
        bid = Bid(bid=int(price), user=currentUser)
        bid.save()

        newListing = Listing(
            title=title,
            description=description,
            imageUrl=imageUrl,
            price=bid,
            isActive = True,
            category=categoryData,
            owner=currentUser,
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))
        
    
    

def listing(request, id):
    listingData = get_object_or_404(Listing, pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = False
    if listingData.owner: 
        isOwner = request.user.username == listingData.owner.username if request.user.is_authenticated else False
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
    })
    
@login_required
def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwner = request.user.username == listingData.owner.username
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)  # Retrieve all comments for the listing

    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "message": "Your auction is closed",
        "update": True,      
    })
    


@login_required
def addBid(request, id):
    if 'newBid' in request.POST:
        newBid = request.POST['newBid']
        listingData = get_object_or_404(Listing, pk=id)

        # Check if price exists and handle if it's None
        if listingData.price is None:
            listingData.price = Bid.objects.create(user=request.user, bid=0)  # Initialize price with a bid of 0
   
        
        isListingInWatchlist = request.user in listingData.watchlist.all()
        allComments = Comment.objects.filter(listing=listingData)
        isOwner = False
        if listingData.owner: 
            isOwner = request.user.username == listingData.owner.username if request.user.is_authenticated else False
        
        # Ensure that the new bid is greater than the current bid
        if int(newBid) > listingData.price.bid:
            updateBid = Bid(user=request.user, bid=int(newBid))
            updateBid.save()
            listingData.price = updateBid  # Update the price with the new bid
            listingData.save()

            # Assuming `allComments` is defined elsewhere, include it in the render context
            return render(request, "auctions/listing.html", {
                "listing": listingData,
                "isListingInWatchlist": isListingInWatchlist,
                "allComments": allComments,  # Ensure allComments is defined
                "isOwner": isOwner,
                "message": "Bid was updated successfully",
                "update": True,
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listingData,
                "isListingInWatchlist": isListingInWatchlist,
                "allComments": allComments,  # Ensure allComments is defined
                "isOwner": isOwner,
                "message": "Your bid must be higher than the current bid.",
                "update": False,
            })
    else:
        return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def AddComment(request, id):
    if request.method == "POST":
        currentUser = request.user
        listingData = get_object_or_404(Listing, pk=id)
        message = request.POST["newComment"]

        newComment = Comment(
            commenter=currentUser,
            listing=listingData,
            message=message,
        )
        newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required
def showWatchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required
def deleteWatchlist(request, id):
    listingData = get_object_or_404(Listing, pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required
def addWatchlist(request, id):
    listingData = get_object_or_404(Listing, pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/register.html")
