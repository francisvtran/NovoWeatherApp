from django.test  import TestCase, Client
from weather.models import City
from django.urls import reverse

#Views Unit Tests to simulate GET and POST requests

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.city = City.objects.create(name='Bethesda', zip_code='20810')

    def test_index_view_get(self):
        response = self.client.get(reverse('index'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/index.html')
        self.assertContains(response, 'What\'s the weather like?')

