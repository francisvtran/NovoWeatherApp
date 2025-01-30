from django.test import TestCase
from weather.forms import LocationForm
from weather.models.location import Location

class LocationFormTest(TestCase):
    def assertInvalidZipCode(self, zip_code, error_msg):
        """Helper function to test invalid ZIP codes"""
        form = LocationForm(data={'zip_code': zip_code})
        self.assertFalse(form.is_valid())
        self.assertIn('zip_code', form.errors)
        self.assertEqual(form.errors['zip_code'][0], error_msg)

    def test_valid_zip_code(self):
        form = LocationForm(data={'zip_code': '20810'})
        self.assertTrue(form.is_valid())

    def test_invalid_zip_code_non_numeric(self):
        self.assertInvalidZipCode('ABCDE', "Enter a valid 5-digit U.S. ZIP Code.")

    def test_invalid_zip_code_symbols(self):
        self.assertInvalidZipCode('!@#$%', "Enter a valid 5-digit U.S. ZIP Code.")

    def test_invalid_zip_code_short(self):
        self.assertInvalidZipCode('123', "Enter a valid 5-digit U.S. ZIP Code.")

    def test_duplicate_zip_code(self):
        """ Ensure duplicate ZIP codes are not allowed on the same day """
        Location.objects.create(name="Test City", zip_code='20810', temp_min=50, temp_max=70)  
        form = LocationForm(data={'zip_code': '20810'})
        self.assertFalse(form.is_valid())
        self.assertIn('zip_code', form.errors)
