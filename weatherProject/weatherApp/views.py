from django.shortcuts import render

import urllib.request
import json
from weatherApp.DB import methods
import sqlite3
import random
from plotly.offline import plot
from plotly.graph_objs import Scatter
# Create your views here.

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&appid=1aeefeae2f95b2296134530e8fce9ecc').read()
        list_of_data = json.loads(source)
        data = {
            "city" : city,
            "country_code" : str(list_of_data['sys']['country']),
            "coordinate" : str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
            "temp" : str(list_of_data['main']['temp']) + ' °C',
            "pressure" : str(list_of_data['main']['pressure']),
            "humidity" : str(list_of_data['main']['humidity']),
            "main" : str(list_of_data['weather'][0]['main']),
            "description" : str(list_of_data['weather'][0]['description']),
            "icon" : list_of_data['weather'][0]['icon'],
        }
        d = random.randint(1, 30)
        if d<10:
            dt = '2021-11-0'+str(d)
        else:
            dt = dt = '2021-11-'+str(d)
        methods.addToDatabase(city, data, dt)
    else:
        data = {}
    return render(request, 'main/index.html', data)


def converter(request):
    # if request.method == 'POST':
    #     data = request.POST.get('')
    values = {"c":"sfsdfs"}
    if request.method == 'POST':
        f = request.POST['F']
        c = request.POST['F']
        values["fah"] = f
        # if request.POST.get("fah"):
        #     fah = form.cleaned_data.get("F")
        #     # cel = form.cleaned_data.get("C")
        #     values["fah"] = fah
        #     # values["cel"] = cel
        #     # c = (fah - 32) * 5 / 9
        #     # cel.initial['C'] = c
            
        # elif request.POST.get("cel"):  
        #     cel = form.cleaned_data.get("C")


    # context= {'fah': fah, 'cel':cel}
    return render(request, 'main/converter.html', values)

def statistics(request):
    sqliteConnection = sqlite3.connect('../../../weatherDB.db')
    c = sqliteConnection.cursor()
    c.execute("select city, Country_Code, Coordinate, Temperature, Pressure, Humidity, Forecast, Description, COUNT(city) as ct from weatherDB group by city order by ct DESC LIMIT 1")

    
    dt = c.fetchall()
    
    context = dict()
    for row in dt:
        context["city"] = row[0]
        context["Country_Code"] = row[1]
        context["Coordinate"] = row[2]
        context["Temperature"] = row[3]
        context["Pressure"] = row[4]
        context["Humidity"] = row[5]
        context["Forecast"] = row[6]
        context["Description"] = row[7]

    c.execute("SELECT Temperature, Date FROM weatherDB WHERE city='" + context['city'] + "' ORDER BY Date ASC")
    dt = c.fetchall()
    context["start_date"] = dt[0][1]
    context["end_date"] = dt[len(dt)-1][1]
    temps = []
    dates = []
    for row in dt:
        temps.append(row[0])
        dates.append(row[1])
    x_data = dates
    y_data = temps
    plot_div = plot([Scatter(x=x_data, y=y_data,
                            mode='lines', name='test',
                            opacity=0.8, marker_color='green')],
                output_type='div')
    context["plot_div"] = plot_div
    return render(request, 'main/statistics.html',context)