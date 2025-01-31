from django.shortcuts import render
from django.conf import settings
from weather.models.location import Location
from weather.forms import LocationForm
import datetime
import requests
import logging

logger = logging.getLogger(__name__)
API_URL = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=imperial'
API_KEY = settings.OWM_API_KEY

def fetch_weather_data(zip_code: str):
    if not API_KEY:
        logger.error("OpenWeatherMap API key is missing. Check your settings.")
        raise ValueError("Weather service unavailable. Please try again later.")

    try:
        #Fetch weather data from OpenWeather API for a given ZIP code.
        response = requests.get(API_URL.format(f"{zip_code},us") + f"&appid={API_KEY}", timeout=5)
        response.raise_for_status()  # Raise HTTPError for 4xx/5xx responses
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise RuntimeError("Location not found. Please enter a valid U.S. ZIP Code.")

    try:
        #Returns a dictionary with city name, min temp, max temp, and icon.
        city_weather_object = response.json()
        city_weather_list = city_weather_object.get("list")
        city_name = city_weather_object.get("city").get("name")
        city_return_list = []
        for city_weather in city_weather_list:
            city_date_txt = city_weather.get("dt_txt")
            if "21:00:00" in city_date_txt:
                city_return_list.append({
                    "name": city_name,
                    "temp_min": city_weather["main"]["temp_min"],
                    "temp_max": city_weather["main"]["temp_max"],
                    "icon": city_weather["weather"][0]["icon"],
                    "date": city_weather["dt"]
                })
        return city_return_list
    #Raises ValueError or RuntimeError for API issues.
    except (KeyError, TypeError, ValueError) as e:
        logger.error(f"Invalid API response: {e}, Response: {response.text}")
        raise RuntimeError("Unexpected response from weather service. Please try again later.")


def save_weather_data(zip_code: str):
    """
    Calls `fetch_weather_data` and saves the weather details to the database.
    Handles errors gracefully.
    """
    try:
        weather_data_list = fetch_weather_data(zip_code)
        for weather_data in weather_data_list:
            Location.objects.create(
                name=weather_data["name"],
                zip_code=zip_code,
                temp_min=weather_data["temp_min"],
                temp_max=weather_data["temp_max"],
                icon=weather_data["icon"],
                date=datetime.datetime.fromtimestamp(weather_data.get("date"))
            )
    except RuntimeError as err:
        raise RuntimeError(str(err))


def index(request):
    """
    Handles GET and POST requests for weather lookups.
    Fetches weather data based on ZIP code input.
    """
    locations = Location.objects.order_by('-id')
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

    context = {'locations': locations, 'form': form, 'error_message': error_message}
    return render(request, 'weather/index.html', context)
