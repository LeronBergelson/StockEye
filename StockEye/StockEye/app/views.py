"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import UserData, WatchList

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
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'app/registration.html', {'form':form})

@login_required
def edit_watchlist(request, id):
    """
    Page where Users can add/remove Stocks from a specific Watchlist 
    
    Parameters:
        id  -   The id of the Watchlist to edit (int)
    """
    assert isinstance(request, HttpRequest)

    stocks = []

    try:
        # Get the user's watchlist that matches the provided id
        watchlist = WatchList.objects.filter(user=request.user, watchList_id=id).get()
        watchlist_id = watchlist.watchList_id

        for stock in watchlist.stockResults.all():
            stocks.append(stock)

        print(f'Stocks: {stocks}')

    except WatchList.DoesNotExist:
        # Given an invalid watchlist id
        # For now, redirect to the watchlists page
        # TODO: Possibly change the behaviour of invalid ids (maybe 
        #       show a message on the watchlists page that a watchlist 
        #       with the given id doesn't exist?)
        return redirect('watchlists')
    
    context = {
        'title': 'Edit Watchlist',
        'year': datetime.now().year,
        'user': request.user,
        'watchlist_id': watchlist_id,
        'stocks': stocks,
    }

    return render(
        request,
        'app/edit_watchlist.html',
        context
    )

@login_required
def watchlists(request):
    """ Renders the watchlists page """
    """
    Alternative to @login_required decorator: manually test with:
        request.user.is_authenticated
    """
    assert isinstance(request, HttpRequest)

    # Since these can throw Django errors if they don't exist, catch them
    try:
        # Get all of the user's watchlists
        watchlists = WatchList.objects.filter(user=request.user).all()
        
        # Store the stocks in each watchlist in a dictionary
        # Each key is the watchList_id from the user's watchlists
        # Each value is a list of Stocks present in the watchlist
        stocks = {}

        for w in watchlists:
            for stock in w.stockResults.all():
                # Check if this is the first stock of the watchlist
                if w.watchList_id in stocks.keys():
                    # Already present, append to list at this key
                    stocks[w.watchList_id].append(stock)
                else:
                    # Key not in dict, set key and create list for this stock
                    stocks[w.watchList_id] = [stock]
                    # stock is of type StockList(models.Model) which is 
                    # not iterable, so use [] instead of list()        

    except UserData.DoesNotExist:
        # Unable to find a matching user, default to no watchlists & stocks
        watchlists = None
        stocks = None
 
    # Additional data to pass to the templating engine
    context = {
        'title':'Watchlists',
        'message':'Your Watchlist page.',
        'year':datetime.now().year,
        'user': request.user,
        'watchlists': watchlists,   # Not sure if this is really needed 
                                    # since the stocks dict has the 
                                    # watchlist_id as its keys
        'stocks': stocks,
        # Previously included the watchlist ids, but since the keys of the 
        # stock dict *are* the watchlist_ids, no need to include them
    }

    return render(
        request,
        'app/watchlists_test.html',
        context
    )