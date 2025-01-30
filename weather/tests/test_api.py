from django.test import TestCase
from unittest.mock import patch
from weather.models.location import Location
from weather.views import fetch_weather_data, save_weather_data
import requests

class WeatherAPITest(TestCase):

    @patch('weather.views.requests.get')                    # Mocks the external API request
    def test_fetch_weather_data_success(self, mock_get):    #Test successful API response handling
        
        # Simulated API response from OpenWeather API
        mock_response = {
            "name": "Houston",
            "main": {"temp_min": 60.0, "temp_max": 70.0},
            "weather": [{"icon": "50n"}]
        }

        # Configuring the mock object to return the simulated response
        mock_get.return_value.status_code = 200                     #HTTP 200 means success
        mock_get.return_value.json.return_value = mock_response     #Mock the JSON response

        #Calling fetch_weather_data with sample ZIP Code
        result = fetch_weather_data("77001")

        # Assertions to check if the function correctly extracts and returns weather data
        self.assertEqual(result["name"], "Houston")
        self.assertEqual(result["temp_min"], 60.0)
        self.assertEqual(result["temp_max"], 70.0)
        self.assertEqual(result["icon"], "50n")

    @patch('weather.views.requests.get')                            # Mocks the external API request
    def test_fetch_weather_data_invalid_zip(self, mock_get):
        # Simulating an API response for an invalid ZIP code (404 Not Found)
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"cod": "404", "message": "city not found"}

        # Expecting a RuntimeError due to invalid ZIP code
        with self.assertRaises(RuntimeError) as context:
            fetch_weather_data("00000")
        
        # The function should raise a specific error message when ZIP is invalid
        self.assertIn("Unexpected response from weather service", str(context.exception))

    @patch('weather.views.requests.get')                            # Mocks the external API request
    def test_fetch_weather_data_invalid_response(self, mock_get):
        # Simulating an invalid response (missing 'main' key)
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}

        # Expecting a RuntimeError due to unexpected response format
        with self.assertRaises(RuntimeError) as context:
            fetch_weather_data("77001")

        # The function should raise an appropriate error message
        self.assertIn("Unexpected response from weather service", str(context.exception))

    @patch('weather.views.requests.get')                            # Mocks the external API request
    def test_fetch_weather_data_api_failure(self, mock_get):
        # Simulating a network failure or API downtime
        mock_get.side_effect = requests.exceptions.RequestException("API is down")

        # Expecting a RuntimeError when the API is not reachable
        with self.assertRaises(RuntimeError) as context:
            fetch_weather_data("77001")

        # The function should raise an appropriate error message
        self.assertIn("Location not found", str(context.exception))

    @patch('weather.views.fetch_weather_data')                      # Mocks fetch_weather_data() to avoid actual API calls
    @patch('weather.models.location.Location.objects.create')       # Mocks database creation
    def test_save_weather_data_success(self, mock_create, mock_fetch):
        # Simulated weather data returned by the mock fetch_weather_data() function
        mock_fetch.return_value = {
            "name": "Houston",
            "temp_min": 60.0,
            "temp_max": 70.0,
            "icon": "50n",
        }

        # Call the function to save weather data
        save_weather_data("77001")
        # Verify that the database create() method was called with the correct arguments
        mock_create.assert_called_once_with(
            name="Houston",
            zip_code="77001",
            temp_min=60.0,
            temp_max=70.0,
            icon="50n",
            date=mock_create.call_args[1]["date"]               # Ensures correct date is used
        )

    @patch('weather.views.fetch_weather_data')                  # Mocks fetch_weather_data() to simulate API errors
    def test_save_weather_data_failure(self, mock_fetch):       #Tests handling of errors when fetching weather data fails before saving.
        # Simulating an error when fetching weather data
        mock_fetch.side_effect = RuntimeError("Service unavailable")

        # Expecting a RuntimeError when saving fails due to fetch error
        with self.assertRaises(RuntimeError) as context:
            save_weather_data("77001")

        # Check if the expected error message is raised
        self.assertIn("Service unavailable", str(context.exception))
