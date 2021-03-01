from django.shortcuts import render

def home(request):
    token = 'pk_d292e121839c4a78b372fbf259af6167'
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

def get_stock_history(request):

    return render(request, 'get_stock_history.html', {})