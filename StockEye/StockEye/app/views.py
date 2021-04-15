"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import UserData, WatchList, StockList
from .forms import CreateWatchListForm, UserChangeForm, EditWatchListForm

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
    assert isinstance(request, HttpRequest)
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    context = {
        'title': 'Register',
        'form': form,
        'year': datetime.now().year,
    }
    
    return render(request, 'app/registration.html', context)

@login_required
def account_settings(request):
    """
    Allows Users to edit their account info, such as their email and password.

    Implementation of the AccountSettingsView.
    """
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST["password"])
            user.save()
            login(request, user)
    else:
        form = UserChangeForm()
        
    context = {
        'title': 'User Profile',
        'message': 'Edit Account Settings',
        'year': datetime.now().year,
        'user': request.user,
        'form': form,
    }

    return render(
        request,
        'app/accountSettings.html',
        context,
    )

def trending(request):
    """renders the trending page"""
    assert isinstance(request, HttpRequest)
    try:
        stocks = StockList.objects.all()
        hold = []
        count = 0
    except StockList.DoesNotExist:
        return print("No Stocks Available")



    while len(hold) < 8:
        for  stock in stocks:
            stock.trend = stock.positiveSentimentCount + stock.negativeSentimentCount
            if stock.trend>= count:
               hold.append(stock)
               count = stock.trend
               
            

    context = {
        'title': 'Trending',
        'year': datetime.now().year,
        'user': request.user,
        'stocks': stocks,
        'hold': hold,

    }

    
    return render(
        request,
        'app/trending.html',
        context,
    )

def stocks(request):
    """
    Displays all stocks. User is able to filter stocks, using buttons 
    provided to the user, by Price, Sentiment, and StockName. All of 
    these filters can be toggled to be in either ascending or descending order.

    Direct implementation of the FilterStockView.
    """

    try:
        stocks = StockList.objects.all()
    except StockList.DoesNotExist:
        stocks = None

    context = {
        'title': 'Filter Stocks',
        'year': datetime.now().year,
        'user': request.user,
        'stocks': stocks,
    }

    return render(
        request,
        'app/stocksview.html',
        context,
    )

def stock(request, s_id):
    """
    Displays the selected stock, providing the name, sentiment, and the price of said stock.

    Direct implementation of the StockView.

    Parameters: s_id - is the id of the desired stock to view.
    """
    assert isinstance(request, HttpRequest)

    try:
        #Get the requested stock with (stock_id)
        stocks = StockList.objects.filter(stock_id=s_id).get()
        stock_id = stocks.stock_id
        stock_name = stocks.symbol
        stock_value = stocks.value
        #do we have a sentiment object?

    except StockList.DoesNotExist:
        #If no stock is not found, returns to stock view to search for new one.
        return redirect('stock')
   
    context = {
        'title': 'Stocks',
        'year': datetime.now().year,
        'user': request.user,
        'stock_id': stock_id,
        'stock_name': symbol,
        'stock_value': value,
    }

    return render(
        request,
        'app/stock.html',
        context
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
        # Handling deleting Watchlist(s)
        if request.method == "POST":
            # Get list of selected checkmark boxes
            watchlists_to_delete = request.POST.getlist('delWatchListId')
            for watchlist_id in watchlists_to_delete:
                # Grab the specified watchlist from the database
                watchlist = WatchList.objects.filter(user=request.user, watchList_id=watchlist_id).get()
                watchlist.delete()
        # User just loads this page again, so grab their (newly updated) WatchLists
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

    # Get the user's watchlist that matches the provided id
    try:
        watchlist = WatchList.objects.filter(user=request.user, watchList_id=w_id).get()
        watchlist_id = watchlist.watchList_id
        watchlist_name = watchlist.watchList_name

        stocks = []

    except WatchList.DoesNotExist:
        # Given an invalid watchlist id
            # For now, redirect to the watchlists page
            # TODO: Possibly change the behaviour of invalid ids (maybe 
            #       show a message on the watchlists page that a watchlist 
            #       with the given id doesn't exist?)
            return redirect('watchlists')

    if request.method == 'POST':
        form = EditWatchListForm(request.POST, instance=watchlist)
        if form.is_valid:
            updated_watchlist = form.save(commit=False)
            updated_watchlist.watchList_id = watchlist_id
            updated_watchlist.user = request.user
            updated_watchlist.name = watchlist_name
            updated_watchlist.save()
            form.save_m2m()
    else:

        form = EditWatchListForm(instance=watchlist)

    for stock in watchlist.stockResults.all():
        stocks.append(stock)

    print(f'Stocks: {stocks}')

    context = {
        'title': 'Edit Watchlist',
        'year': datetime.now().year,
        'user': request.user,
        'watchlist_id': watchlist_id,
        'watchlist_name': watchlist_name,
        'stocks': stocks,
        'form': form,
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

    print(f'Watchlists:{watchlists}\tStocks:{stocks}')

    if watchlists.count() != 0 and len(stocks) != 0:
        watchlist_stocks = zip(watchlists, stocks)
    else:
        watchlist_stocks = None

    context = {
        'title':'Watchlists',
        'message':'Your Watchlist page.',
        'year':datetime.now().year,
        'user': request.user,
        'data': watchlist_stocks,
    }

    return render(
        request,
        'app/watchlists.html',
        context
    )
