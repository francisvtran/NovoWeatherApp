from django.shortcuts import render
from django.conf import settings
import requests

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial'
    
    appid = settings.OWM_API_KEY

    if not appid:
        raise ValueError("OpenWeatherMap API key is not set. Check your settings.")

    zip_code = '20810,us'

    city_weather = requests.get(url.format(zip_code) + f"&appid={appid}").json()

    weather = {
        'city' : city_weather['name'],
        'temp_min' : city_weather['main']['temp_min'],
        'temp_max' : city_weather['main']['temp_max'],
        'icon' : city_weather['weather'][0]['icon']
    }

    context = {'weather' : weather}

    return render(request, 'weather/index.html', context)
