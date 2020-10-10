from django.shortcuts import render
from .models import Stock

def home(request):
    import requests
    import json 

    if request.method == 'POST':
        ticker = request.POST ['ticker']
        api_request = requests.get ("https://cloud.iexapis.com/stable/stock/"  + ticker + "/quote?token=pk_61ca93bb27b54f39915de255562e1cdd")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api= "Error..."
        return render(request, 'home.html', {'api': api})
            
    else:
        return render(request, 'home.html', {'ticker': "Enter a Stock Symbol Above .."})
        

    

def about (request):
    return  render(request, 'about.html', {})

def add_stock (request):

    ticker = Stock.objects.all()
    return  render(request, 'add_stock.html', {'ticker': ticker})