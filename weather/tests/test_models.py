from django.test import TestCase
from weather.models import City
from django.core.exceptions import ValidationError

#Models Unit Tests testing behavior of City model
class CityModelTest(TestCase):
    #Does __str__ correctly return the city name?
    def test_city_str_method(self):
        city = City.objects.create(name='Bethesda', zip_code='20810')
        self.assertEqual(str(city), 'Bethesda')

    def test_create_city(self):
        city = City.objects.create(name='Rockville', zip_code='20852')
        self.assertIsInstance(city, City)
        self.assertEqual(city.name, 'Rockville')
        self.assertEqual(city.zip_code, '20852')

    def test_default_zip_code(self):
        city = City.objects.create(name='Silver Spring')
        self.assertEqual(city.zip_code, '00000')  

    def test_multiple_cities(self):
        city1 = City.objects.create(name='Gaithersburg', zip_code='20878')
        city2 = City.objects.create(name='Takoma Park', zip_code='20912')
        self.assertEqual(City.objects.count(), 2)

    def test_invalid_zip_code_short(self):
        city = City(name='InvalidCity', zip_code='1234')  
        with self.assertRaises(ValidationError):  
            city.full_clean()

    def test_invalid_zip_code_long(self):
        city = City(name='InvalidCity', zip_code='123456')  
        with self.assertRaises(ValidationError):  
            city.full_clean()





