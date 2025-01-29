from django.shortcuts import render
from django.conf import settings
from weather.models.location import Location
from weather.models.locationdto import LocationDTO
from weather.forms import CityForm
import requests

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial'
appid = settings.OWM_API_KEY

def get_weather_data(locations: list[Location]) -> list[LocationDTO]:
    weather_data: list[LocationDTO] = []
    for location in locations:
        response = requests.get(url.format(f"{location.zip_code},us") + f"&appid={appid}")
    
        if response.status_code == 200:
            city_weather = response.json()

            # Check if the API response contains the required keys
            if 'name' in city_weather and 'main' in city_weather and 'weather' in city_weather:
                weather: LocationDTO = {
                    'city': city_weather['name'],
                    'temp_min': city_weather['main']['temp_min'],
                    'temp_max': city_weather['main']['temp_max'],
                    'icon': city_weather['weather'][0]['icon']
                }
                weather_data.append(weather)

            else:
                # Handle incomplete or unexpected responses
                raise RuntimeError(f"Invalid data for {location.zip_code}")
                
        else:
            # Handle API errors (e.g., invalid ZIP code or server issues)
            raise RuntimeError(response.json().get('message', 'Unknown error'))
    return weather_data

def save_weather_data(zip_code: str):
    if not appid:
        raise ValueError("OpenWeatherMap API key is not set. Check your settings.")
    
    # Fetch city name from API
    response = requests.get(url.format(f"{zip_code},us") + f"&appid={appid}")

    if response.status_code == 200:
        city_weather = response.json()
        city_name = city_weather.get('name', 'Unknown City')  # Default to 'Unknown City' if missing
                
        # Save city with name and ZIP code
        Location.objects.create(name=city_name, zip_code=zip_code)

    else:
        raise RuntimeError("ZIP Code does not exist. Please enter a valid U.S. ZIP Code.")

def index(request):
    locations = Location.objects.all().order_by('-id')
    error_message = None
    weather_data  = None

    if request.method == 'POST': 
        form = CityForm(request.POST) 
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']   
            try:
                save_weather_data(zip_code)
            except RuntimeError as err:
                error_message = str(err)
    else:
        form = CityForm()

    try:
        weather_data = get_weather_data(locations)
    except RuntimeError as err:
        error_message += str(err)
    context = {'weather_data' : weather_data, 'form' : form, 'error_message': error_message}
    return render(request, 'weather/index.html', context)

