from django.shortcuts import render
from django.conf import settings
import requests

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial'
    
    appid = settings.OWM_API_KEY

    if not appid:
        raise ValueError("OpenWeatherMap API key is not set. Check your settings.")

    city = 'Bethesda'

    city_weather = requests.get(url.format(city) + f"&appid={appid}").json()

    print(city_weather)  #comment this out later

    return render(request, 'weather/index.html')
