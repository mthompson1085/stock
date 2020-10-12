from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import pandas as pd
from math import pi
import datetime
from .utils import get_data, convert_to_df

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

def add_stock(request):
    import requests
    import json 

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added"))
            return redirect ('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/"  + str(ticker_item) + "/quote?token=pk_61ca93bb27b54f39915de255562e1cdd")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api= "Error..."
        return  render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete (request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted"))
    return redirect (delete_stock)

def delete_stock (request):
    ticker = Stock.objects.all()
    return  render(request, 'delete_stock.html', {'ticker':ticker})

def homepage(request):

    result = get_data('goog','anzn', 'pk_61ca93bb27b54f39915de255562e1cdd ')
    source = convert_to_df(result)

    increasing = source.close > source.open
    decreasing = source.open > source.close
    w = 12 * 60 * 60 * 1000

    TOOLS = "pan, wheel_zoom, box_zoom, reset, save"
    title = 'EUR to USD chart'

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=700, plot_height=500, title = title)
    p.xaxis.major_label_orientation = pi / 4

    p.grid.grid_line_alpha = 0.3

    p.segment(source.date, source.high, source.date, source.low, color="black")
    p.vbar(source.date[increasing], w, source.open[increasing], source.close[increasing],
        fill_color="#D5E1DD", line_color="black"
    )
    p.vbar(source.date[decreasing], w, source.open[decreasing], source.close[decreasing], 
        fill_color="#F2583E", line_color="black"
    )

    script, div = components(p)

    return render(request,'add_stock.html',{'script':script, 'div':div })


