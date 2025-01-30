from django.test import TestCase
from weather.models.location import Location
from django.core.exceptions import ValidationError

class LocationModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.city = Location.objects.create(name='Bethesda', zip_code='20810', temp_min=50, temp_max=75)

    def test_city_str_method(self):
        city = Location.objects.create(name='Bethesda', zip_code='20810', temp_min=55, temp_max=80)
        self.assertEqual(str(city), 'Bethesda')
        

    def test_create_location(self):
        location = Location.objects.create(name='Rockville', zip_code='20852', temp_min=60, temp_max=85)
        self.assertIsInstance(location, Location)
        self.assertEqual(location.zip_code, '20852')

    def test_multiple_locations(self):
        Location.objects.create(name='Gaithersburg', zip_code='20878', temp_min=45, temp_max=68)
        Location.objects.create(name='Takoma Park', zip_code='20912', temp_min=49, temp_max=72)
        self.assertEqual(Location.objects.count(), 3)  # Including setUp city

    def test_invalid_zip_code_short(self):
        location = Location(name='InvalidCity', zip_code='1234')
        with self.assertRaisesMessage(ValidationError, "ZIP code must be exactly 5 digits."):
            location.full_clean()

    def test_invalid_zip_code_long(self):
        location = Location(name='InvalidCity', zip_code='123456')
        with self.assertRaisesMessage(ValidationError, "ZIP code must be exactly 5 digits."):
            location.full_clean()
