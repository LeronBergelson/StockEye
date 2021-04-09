"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

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

def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'app/registration.html', {'form':form})

def trending(request):
    """renders the trending page"""
    assert isinstance(request, HttpRequest)
    return render (
        request,
        'app/trending.html',
        {
            'title': 'Trending',
            'message': 'Your trending page',
            'year': datetime.now().year,
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