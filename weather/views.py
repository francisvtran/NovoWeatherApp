from django.shortcuts import render
from django.conf import settings
from weather.models.location import Location
from weather.models.locationdto import LocationDTO
from weather.forms import LocationForm
import datetime
import requests
import logging

logger =  logging.getLogger(__name__)
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial'
appid = settings.OWM_API_KEY

def save_weather_data(zip_code: str):
    """This is an example of an API response for Houston, TX
    {"coord":{"lon":-95.3633,"lat":29.7633},"weather":[{"id":701,"main":"Mist","description":"mist","icon":"50n"}],
    "base":"stations","main":{"temp":66.36,"feels_like":67.03,"temp_min":62.58,"temp_max":69.21,"pressure":1015,
    "humidity":92,"sea_level":1015,"grnd_level":1012},"visibility":4023,"wind":{"speed":11.5,"deg":130},"clouds":
    {"all":100},"dt":1738198209,"sys":{"type":2,"id":2001415,"country":"US","sunrise":1738156368,"sunset":1738194977}
    ,"timezone":-21600,"id":4699066,"name":"Houston","cod":200}"""

    if not appid:
        raise ValueError("OpenWeatherMap API key is not set. Check your settings.")
    
    # Fetch city name from API
    response = requests.get(url.format(f"{zip_code},us") + f"&appid={appid}")

    if response.status_code == 200:
        city_weather = response.json()
        city_name = city_weather.get('name', 'Unknown City')  # Default to 'Unknown City' if missing
        try:
            city_temp_min = city_weather['main']['temp_min']
            city_temp_max = city_weather['main']['temp_max']
        except KeyError as e:
            logger.error(f"Data was not as expected. {e}")
            raise e
    
        # Save city with name and ZIP code
        Location.objects.create(name=city_name, zip_code=zip_code, temp_min=city_temp_min, temp_max=city_temp_max)

    else:
        raise RuntimeError("ZIP Code does not exist. Please enter a valid U.S. ZIP Code.")

#index view 
def index(request):
    locations = Location.objects.filter(date=datetime.date.today()).order_by('-id') #initial query
    error_message = None

    if request.method == 'POST': 
        form = LocationForm(request.POST) 
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']   
            try:
                save_weather_data(zip_code)
            except RuntimeError as err:
                error_message = str(err)
    else:
        form = LocationForm()

    context = {'locations' : locations, 'form' : form, 'error_message': error_message}
    return render(request, 'weather/index.html', context)

