from django.test import TestCase
from unittest.mock import patch
from weather.models.location import Location
from weather.views import fetch_weather_data, save_weather_data
import requests

class WeatherAPITest(TestCase):

    @patch('weather.views.requests.get')
    def test_fetch_weather_data_success(self, mock_get):
        """Test successful API response handling"""
        mock_response = {
            "name": "Houston",
            "main": {"temp_min": 60.0, "temp_max": 70.0},
            "weather": [{"icon": "50n"}]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = fetch_weather_data("77001")

        self.assertEqual(result["name"], "Houston")
        self.assertEqual(result["temp_min"], 60.0)
        self.assertEqual(result["temp_max"], 70.0)
        self.assertEqual(result["icon"], "50n")

    @patch('weather.views.requests.get')
    def test_fetch_weather_data_invalid_zip(self, mock_get):
        """Test API error for invalid ZIP code"""
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"cod": "404", "message": "city not found"}

        with self.assertRaises(RuntimeError) as context:
            fetch_weather_data("00000")
        
        self.assertIn("Unexpected response from weather service", str(context.exception))

    @patch('weather.views.requests.get')
    def test_fetch_weather_data_invalid_response(self, mock_get):
        """Test unexpected API response format"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}

        with self.assertRaises(RuntimeError) as context:
            fetch_weather_data("77001")

        self.assertIn("Unexpected response from weather service", str(context.exception))

    @patch('weather.views.requests.get')
    def test_fetch_weather_data_api_failure(self, mock_get):
        """Test API request failure handling"""
        mock_get.side_effect = requests.exceptions.RequestException("API is down")

        with self.assertRaises(RuntimeError) as context:
            fetch_weather_data("77001")

        self.assertIn("Location not found", str(context.exception))

    @patch('weather.views.fetch_weather_data')
    @patch('weather.models.location.Location.objects.create')
    def test_save_weather_data_success(self, mock_create, mock_fetch):
        """Test saving valid weather data"""
        mock_fetch.return_value = {
            "name": "Houston",
            "temp_min": 60.0,
            "temp_max": 70.0,
            "icon": "50n",
        }

        save_weather_data("77001")
        mock_create.assert_called_once_with(
            name="Houston",
            zip_code="77001",
            temp_min=60.0,
            temp_max=70.0,
            icon="50n",
            date=mock_create.call_args[1]["date"]
        )

    @patch('weather.views.fetch_weather_data')
    def test_save_weather_data_failure(self, mock_fetch):
        """Test handling error when fetching weather data fails"""
        mock_fetch.side_effect = RuntimeError("Service unavailable")

        with self.assertRaises(RuntimeError) as context:
            save_weather_data("77001")

        self.assertIn("Service unavailable", str(context.exception))
