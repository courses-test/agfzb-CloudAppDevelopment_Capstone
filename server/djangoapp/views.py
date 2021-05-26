from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.conf import settings
from . import models
from . import restapis
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = { 'user': request.user }
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = { 'user': request.user }
    if request.method == "POST":
        pass
    return render(request, 'djangoapp/contact_us.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = { 'user': request.user }
    print(request.method)
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request,'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = { 'user': request.user }
    print(request.method)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['exists'] = True
            return render(request, 'djangoapp/registration_request.html', context)
    else:
        return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = { 'user': request.user }
    if request.method == "GET":
        url = settings.CLOUD_URL + "/dealership"
        # Get dealers from the URL
        dealerships = restapis.get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context['dealers'] = dealerships
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = { 'user': request.user }
    url = settings.CLOUD_URL + "/reviews?dealerId=" + str(dealer_id)
    url_dealer = settings.CLOUD_URL + "/get-dealer?dealerId=" + str(dealer_id)
    reviews = restapis.get_dealer_reviews_from_cf(url)
    context['reviews'] = reviews
    context['dealer_id'] = dealer_id
    dealers_found = restapis.get_dealers_from_cf(url_dealer)
    if len(dealers_found) > 0:
        context['dealer_name'] = dealers_found[0].full_name
    else:
        context['dealer_name'] = ""
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):    
    if request.method == "GET":
        context = dict()
        context['user'] = request.user
        context['dealer_id'] = dealer_id
        context['cars'] = models.CarModel.objects.filter(dealerId=int(dealer_id))
        url_dealer = settings.CLOUD_URL + "/get-dealer?dealerId=" + str(dealer_id)
        dealers_found = restapis.get_dealers_from_cf(url_dealer)
        if len(dealers_found) > 0:
            context['dealer_name'] = dealers_found[0].full_name
        else:
            context['dealer_name'] = ""
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        # Validations
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Please login to post reviews")
        if request.POST['review'] == "":
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

        # Store review
        review = dict()
        review['name'] = request.user.first_name + " " + request.user.last_name
        review["time"] = datetime.utcnow().isoformat()
        review['dealership'] = dealer_id
        review['review'] = request.POST['review']
        if 'purchase' in request.POST:
            # payload if uer purchased a car
            review['purchase'] = True
            review['purchase_date'] = request.POST['date']
            car_id = request.POST['car']
            purchased_car = models.CarModel.objects.get(pk=car_id)
            review['car_make'] = purchased_car.maker.name
            review['car_model'] = purchased_car.name
            review['car_year'] = purchased_car.year.strftime("%Y")
        else:
            review['purchase'] = False
        json_payload = dict()
        json_payload["review"] = review
        result = restapis.post_request(settings.CLOUD_URL + '/reviews', 
            json_payload, apikey=None, dealerId=dealer_id)
        
        # Return result
        return redirect('djangoapp:dealer_details', dealer_id)
        #return HttpResponse(result) 
