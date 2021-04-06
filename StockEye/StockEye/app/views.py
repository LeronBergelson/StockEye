"""
Definition of views.
"""

from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

from .models import UserData

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

@login_required
def watchlists(request):
    """ Renders the watchlists page """
    """
    Alternative to @login_required decorator: manually test with:
        request.user.is_authenticated
    """
    assert isinstance(request, HttpRequest)

    # Get the current user
    user = UserData.objects.filter(user=request.user).get()

    # Get all of the user's watchlists
    watchlists = user.stockResults.all()

    # Additional data to pass to the templating engine
    context = {
        'title':'Watchlists',
        'message':'Your Watchlist page.',
        'year':datetime.now().year,
        'user': request.user,
        'watchlists': watchlists,
    }

    return render(
        request,
        'app/watchlists_test.html',
        context
    )
