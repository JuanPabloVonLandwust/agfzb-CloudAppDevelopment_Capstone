"""Django App Views"""
import logging
import json
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
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
    """Returns the rendered 'Index' page"""
    context = {}
    return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
