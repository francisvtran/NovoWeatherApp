from unittest.mock import patch
from django.test import TestCase
from weather.models import City

#API Unit Tests mocking valid and invalid API requests
class APICallTest(TestCase):
    @patch('requests.get')
    def test_valid_api_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'name': 'Bethesda',
            'main': {
                'temp_min': 55,
                'temp_max': 75
            },
            'weather': [{'icon': '01d'}],
            'sys': {'country': 'US'}
        }

        city = City.objects.create(name='Bethesda', zip_code='20810')
        response = mock_get(f'http://api.openweathermap.org/data/2.5/weather?zip={city.zip_code},us')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Bethesda')

    @patch('requests.get')
    def test_invalid_api_response(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {
            'message': 'city not found'
        }

        city = City.objects.create(name='Invalid City', zip_code='00000')
        response = mock_get(f'http://api.openweathermap.org/data/2.5/weather?zip={city.zip_code},us')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'city not found')