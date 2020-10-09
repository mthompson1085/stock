from django.shortcuts import render

def home(request):
    import requests
    import json 

    #pk_61ca93bb27b54f39915de255562e1cdd
    api_request = requests.get ("https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_61ca93bb27b54f39915de255562e1cdd")

    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api= "Error..."


    return render(request, 'home.html', {'api': api})

def about (request):
    return  render(request, 'about.html', {})