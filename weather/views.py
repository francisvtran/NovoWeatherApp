from django.shortcuts import render
from django.conf import settings
from .models import City
from .forms import CityForm
import requests

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial'
    appid = settings.OWM_API_KEY

    if not appid:
        raise ValueError("OpenWeatherMap API key is not set. Check your settings.")

    cities = City.objects.all().order_by('-id')

    if request.method == 'POST': 
        form = CityForm(request.POST) 
        if form.is_valid():
            form.save() 
        else:
            form = CityForm(request.POST)
    else:
        form = CityForm()

    weather_data = []
    for city in cities:

        city_weather = requests.get(url.format(f"{city.zip_code},us") + f"&appid={appid}").json()

        weather = {
            'city' : city_weather['name'],
            'temp_min' : city_weather['main']['temp_min'],
            'temp_max' : city_weather['main']['temp_max'],
            'icon' : city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/index.html', context)
