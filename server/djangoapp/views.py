"""Django App Views"""
import logging
import json
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealer_by_state, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    """Returns the rendered 'About Us' page"""
    context = {}
    return render(request=request, template_name='djangoapp/about.html', context=context)

# Create a `contact` view to return a static contact page
def contact(request):
    """Returns the rendered 'Contact Us' page"""
    context = {}
    return render(request=request, template_name='djangoapp/contact.html', context=context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    """Logins the user and returns the rendered 'Login' page"""
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect('djangoapp:index')
        context['message'] = 'Invalid username or password'
        return render(request=request, template_name='djangoapp/login.html', context=context)
    return render(request=request, template_name='djangoapp/login.html', context=context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    """Logouts the user and redirects to the index page"""
    logout(request=request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    """Registers a user and returns the rendered 'Registration' page"""
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except ObjectDoesNotExist:
            logger.debug('%s is new user', username)
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name,
                                            last_name=last_name, password=password)
            login(request=request, user=user)
            return redirect('djangoapp:index')
        context['message'] = 'User already exists.'
        return render(request=request, template_name='djangoapp/registration.html',
                        context=context)
    return render(request=request, template_name='djangoapp/registration.html', context=context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == 'GET':
        url = 'https://us-south.functions.appdomain.cloud/api/v1/web/b6f51563-5d32-4072-be12-2a82e881e0a8/dealership-package/get-dealership.json'
        id = request.GET.get('id')
        if id:
            dealership = get_dealer_by_id(url=url, id=id)
            return HttpResponse(dealership)
        state = request.GET.get('state')
        if state:
            dealerships = get_dealer_by_state(url=url, state=state)
            dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
            return HttpResponse(dealer_names)
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url=url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    # """Returns the rendered 'Index' page"""
    # context = {}
    # return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    if request.method == 'GET':
        url = 'https://us-south.functions.appdomain.cloud/api/v1/web/b6f51563-5d32-4072-be12-2a82e881e0a8/dealership-package/get-review.json'
        reviews = get_dealer_reviews_from_cf(url=url, dealership=dealer_id)
        dealer_reviews = ' '.join([f'{review.review} {review.sentiment}' for review in reviews])
        return HttpResponse(dealer_reviews)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    user = request.user
    if user.is_authenticated:
        # if request.method == 'POST':
            url = 'https://us-south.functions.appdomain.cloud/api/v1/web/b6f51563-5d32-4072-be12-2a82e881e0a8/dealership-package/post-review.json'
            review = {}
            review['car_make'] = 'Renault'
            review['car_model'] = 'Duster'
            review['car_year'] = 2015
            review['name'] = 'Juan Pablo'
            review['purchase'] = True
            review['purchase_date'] = datetime.utcnow().isoformat()
            review['review'] = 'Service was great!'
            json_payload = {}
            json_payload['review'] = review
            json_result = post_request(url=url, json_payload=json_payload, dealership=dealer_id)
            return HttpResponse(json.dumps(json_result, indent=2))
