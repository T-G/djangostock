from django.shortcuts import render, redirect

from decouple import config
from .models import Stock
from django.contrib import messages
from .forms import StockForm

def home(request):
    token = config('API_TOKEN')
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
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added..."))
            return redirect('add_stock')
    
    ticker = Stock.objects.all()
    return render(request, 'quotes/add_stock.html', {'ticker' : ticker})

def delete_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been removed!"))
    return redirect('add_stock')