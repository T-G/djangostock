from django.shortcuts import render, redirect

from decouple import config
from .models import Stock
from django.contrib import messages
from .forms import StockForm

# Stock exchange key
token = config('API_TOKEN')


def home(request):
    # url https://sandbox.iexapis.com/stable/stock/aapl/batch?types=quote,news,chart&range=1m&last=10&token=Tsk_5ae4803c3eba4867ae86df6e747952d0
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get(f'https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={token}')

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error"

        return render(request, 'quotes/home.html', {'api': api})

    else:
        ticker = "Please Enter a Ticker Symbol Above..."
        return render(request, 'quotes/home.html', {'ticker': ticker})
    
def about(request):
    return render(request, 'quotes/about.html', {})


def add_stock(request):
    import requests
    import json

    # IF SOMEONE ENTERS A TICKER IN THE SEARCH BOX
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added..."))
            return redirect(add_stock)
    
    # RETURN TICKER FROM LOCAL DATABASE
    ticker = Stock.objects.all()
    # Variable to store the ticker item in a list
    result = []
    
    # Match the tickers form the database and query the api
    for ticker_item in ticker:
        api_request = requests.get(f'https://cloud.iexapis.com/stable/stock/{ticker_item}/quote?token={token}')
        try:
            api = json.loads(api_request.content)
            result.append(api)
        except Exception as e:
            api = 'Error'
    
    return render(request, 'quotes/add_stock.html', {'ticker' : ticker, 'result':result})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been removed!"))
    return redirect(delete_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    context = {'ticker': ticker}
    return render(request, 'quotes/delete_stock.html', context)