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

    def test_index_view_post_valid_zip_code(self):
        response = self.client.post(reverse('index'), {'zip_code': '12345'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '12345') 

    def test_index_view_post_invalid_zip_code_short(self):
        response = self.client.post(reverse('index'), {'zip_code': '000'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid 5-digit U.S. ZIP Code.')

    def test_index_view_post_invalid_zip_code(self):
        response = self.client.post(reverse('index'), {'zip_code': '00000'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ZIP Code does not exist. Please enter a valid U.S. ZIP Code.')

        