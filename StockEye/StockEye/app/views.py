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
from .forms import CreateWatchListForm, UserChangeForm

def home(request):
    """
    The landing page of the StockEye application.

    Direct implementation of the HomeView.
    """
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
    """
    Provides Users with information on how to contact the StockEye team.

    Does not directly implement a view.
    """
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
    """
    Includes various information about the StockEye project itself.

    Does not directly implement a view.
    """
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
    """
    Allows guest Users to register for an account, allowing them to track 
    Stocks of their choosing in Watchlists.

    Direct implementation of the RegistrationView.
    """
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'app/registration.html', {'form':form})

@login_required
def account_settings(request):
    """
    Allows Users to edit their account info, such as their email and password.

    Implementation of the AccountSettingsView.
    """
    assert isinstance(request, HttpRequest)

    try:
        user = request.user
        change_user_form = UserChangeForm()
        #change_password_form = AdminPasswordChangeForm()
    except UserData.DoesNotExist:
        return redirect('register')
        
    context = {
        'title': 'User Profile',
        'message': 'Edit Account Settings',
        'year': datetime.now().year,
        'user': request.user,
        'form': change_user_form,
    }

    return render(
        request,
        'app/accountSettings.html',
        context,
    )

def search(request):
    """renders the trending page"""
    assert isinstance(request, HttpRequest)
    return render (
        request,
        'app/search.html',
        {
            'title': 'Trending',
            'message': 'Your trending page',
            'year': datetime.now().year,
        }
    )
def stocks(request):
    """
    Displays all stocks. User is able to filter stocks, using buttons 
    provided to the user, by Price, Sentiment, and StockName. All of 
    these filters can be toggled to be in either ascending or descending order.

    Direct implementation of the FilterStockView.
    """



    context = {

    }

    return render(
        request,
        'app/'
    )

@login_required
def create_watchlist(request):
    """
    Allows Users to create a new Watchlist
    """

    # Below loop seems very inefficient, since it querys the database
    # TODO: See if the below loop can be optimized, or another solution
    #       is available.

    # Get the current highest watchList_id
    watchlist = WatchList.objects.latest()
    watchlist_id = watchlist.watchList_id
    watchlist_id += 1

    if request.method == 'POST':
        form = CreateWatchListForm(request.POST)
        if form.is_valid():
            new_watchlist = form.save(commit=False)
            new_watchlist.user = request.user
            new_watchlist.watchList_id = watchlist_id
            new_watchlist.save()
            form.save_m2m()
            return redirect('edit_watchlist', w_id=watchlist_id)

    else:
        # Create a blank form otherwise
        form = CreateWatchListForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'app/create_watchlist.html',
        context,
    )


@login_required
def delete_watchlist(request, w_id):
    """
    Deletes a User's Watchlist where watchList_id=id.
    Redirects to /watchlists/ after execution.
    """
    try:
        watchlist = WatchList.objects.filter(user=request.user).get(watchList_id=w_id)
    except WatchList.DoesNotExist:
        return redirect('watchlists')
    watchlist.delete()
    return redirect('watchlists')

@login_required
def manage_watchlists(request):
    """
    Allows Users to create and delete Watchlists from their account.

    Direct implementation of the ManageWatchlistView.
    """
    assert isinstance(request, HttpRequest)

    try:
        watchlists = WatchList.objects.filter(user=request.user).all()
        
    except WatchList.DoesNotExist:
        watchlists = []

    context = {
        'title': 'Manage Watchlists',
        'year': datetime.now().year,
        'user': request.user,
        'watchlists': watchlists,
    }

    return render(
        request,
        'app/manage_watchlists.html',
        context,
    )


@login_required
def edit_watchlist(request, w_id):
    """
    Page where Users can add/remove Stocks from a specific Watchlist 
    
    Direct implementation of the EditWatchlistView.

    Parameters:
        id  -   The id of the Watchlist to edit (int)
    """
    assert isinstance(request, HttpRequest)

    stocks = []

    try:
        # Get the user's watchlist that matches the provided id
        watchlist = WatchList.objects.filter(user=request.user, watchList_id=w_id).get()
        watchlist_id = watchlist.watchList_id
        watchlist_name = watchlist.watchList_name

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
        'watchlist_name': watchlist_name,
        'stocks': stocks,
    }

    return render(
        request,
        'app/edit_watchlist.html',
        context
    )

@login_required
def watchlists(request):
    """ 
    Page where Users can view their Watchlists.

    Direct implementation of the WatchlistView.
    """

    assert isinstance(request, HttpRequest)

    # Since these can throw Django errors if they don't exist, catch them
    try:
        # Get all of the user's watchlists
        watchlists = WatchList.objects.filter(user=request.user).all()
        
        # Store the stocks in each watchlist in a dictionary
        # Each key is the watchList_name from the user's watchlists
        # Each value is a list of Stocks (as StockList model objects) 
        # present in the watchlist
        stocks = []
        counter = 0

        for w in watchlists:
            stocks.append([])
            for stock in w.stockResults.all():
                # No need to check if key is in the dict, since 
                # it is added above
                stocks[counter].append(stock)
            counter += 1

    except UserData.DoesNotExist:
        # Unable to find a matching user, default to no watchlists & stocks
        watchlists = None
        stocks = None
    
    watchlist_stocks = zip(watchlists, stocks)

    context = {
        'title':'Watchlists',
        'message':'Your Watchlist page.',
        'year':datetime.now().year,
        'user': request.user,
        'data': watchlist_stocks,
    }

    return render(
        request,
        'app/watchlists_test.html',
        context
    )
