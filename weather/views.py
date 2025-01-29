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
    error_message = None

    if request.method == 'POST': 
        form = CityForm(request.POST) 
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']

            # Fetch city name from API
            response = requests.get(url.format(f"{zip_code},us") + f"&appid={appid}")

            if response.status_code == 200:
                city_weather = response.json()
                city_name = city_weather.get('name', 'Unknown City')  # Default to 'Unknown City' if missing
                
                # Save city with name and ZIP code
                City.objects.create(name=city_name, zip_code=zip_code)

            else:
                error_message = "Invalid ZIP Code. Please enter a valid U.S. ZIP Code."

    else:
        form = CityForm()

    weather_data = []
    for city in cities:
        response = requests.get(url.format(f"{city.zip_code},us") + f"&appid={appid}")
    
        if response.status_code == 200:
            city_weather = response.json()

            # Check if the API response contains the required keys
            if 'name' in city_weather and 'main' in city_weather and 'weather' in city_weather:
                weather = {
                    'city': city_weather['name'],
                    'temp_min': city_weather['main']['temp_min'],
                    'temp_max': city_weather['main']['temp_max'],
                    'icon': city_weather['weather'][0]['icon']
                }
                weather_data.append(weather)

            else:
                # Handle incomplete or unexpected responses
                weather_data.append({
                    'city': f"Invalid data for {city.zip_code}",
                    'temp_min': 'N/A',
                    'temp_max': 'N/A',
                    'icon': None
                })
                
        else:
            # Handle API errors (e.g., invalid ZIP code or server issues)
            error_message = response.json().get('message', 'Unknown error')
            if error_message == "city not found":
                weather_data.append({
                    'city': f"Error for {city.zip_code}: Invalid ZIP Code",
                    'temp_min': 'N/A',
                    'temp_max': 'N/A',
                    'icon': None
                })
            else:
                weather_data.append({
                'city': f"Error for {city.zip_code}: {error_message}",
                'temp_min': 'N/A',
                'temp_max': 'N/A',
                'icon': None
                })

    context = {'weather_data' : weather_data, 'form' : form, 'error_message': error_message}
    return render(request, 'weather/index.html', context)

