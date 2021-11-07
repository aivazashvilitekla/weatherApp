from django.shortcuts import render
import urllib.request
import json
from weatherApp.DB import methods
import sqlite3
# Create your views here.

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&appid=1aeefeae2f95b2296134530e8fce9ecc').read()
        list_of_data = json.loads(source)
        data = {
            "country_code" : str(list_of_data['sys']['country']),
            "coordinate" : str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
            "temp" : str(list_of_data['main']['temp']) + ' °C',
            "pressure" : str(list_of_data['main']['pressure']),
            "humidity" : str(list_of_data['main']['humidity']),
            "main" : str(list_of_data['weather'][0]['main']),
            "description" : str(list_of_data['weather'][0]['description']),
            "icon" : list_of_data['weather'][0]['icon'],
        }
        # methods.addToDatabase(city, data)
    else:
        data = {}
    return render(request, 'main/index.html', data)


def converter(request):
    if request.method == 'POST':
        data = request.POST.get('')
    return render(request, 'main/converter.html')

def statistics(request):
    # if request.method == 'POST':
    #     data = request.POST.get('')
    # dt = methods.getViewed()
    
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
    
    return render(request, 'main/statistics.html',context)