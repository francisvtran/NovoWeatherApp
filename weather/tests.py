from django.test import TestCase
from .forms import CityForm

#Form Unit Tests
class CityFormTest(TestCase):
    def test_valid_zip_code(self):
        form = CityForm(data={'zip_code': '20810'})
        self.assertTrue(form.is_valid())

    def test_invalid_zip_code_non_numeric(self):
        form = CityForm(data={'zip_code': 'ABCDE'})  
        self.assertFalse(form.is_valid())
        self.assertIn('zip_code', form.errors)
        self.assertEqual(form.errors['zip_code'][0], "Enter a valid 5-digit ZIP Code.")

    def test_invalid_zip_code_non_numeric_symbols(self):
        form = CityForm(data={'zip_code': '!@#$%'})  
        self.assertFalse(form.is_valid())
        self.assertIn('zip_code', form.errors)
        self.assertEqual(form.errors['zip_code'][0], "Enter a valid 5-digit ZIP Code.")

    def test_invalid_zip_code_short(self):
        form = CityForm(data={'zip_code': '123'})  
        self.assertFalse(form.is_valid())
        self.assertIn('zip_code', form.errors)
        self.assertEqual(form.errors['zip_code'][0], "Enter a valid 5-digit ZIP Code.")

    def test_invalid_zip_code_long(self):
        form = CityForm(data={'zip_code': '123'})  
        self.assertFalse(form.is_valid())
        self.assertIn('zip_code', form.errors)
        self.assertEqual(form.errors['zip_code'][0], "Enter a valid 5-digit ZIP Code.")

    def test_duplicate_zip_code(self):
        # First, save a valid ZIP code to the database
        form = CityForm(data={'zip_code': '20810'})
        if form.is_valid():
            form.save()
        # Attempt to save the same ZIP code again
        form = CityForm(data={'zip_code': '20810'})
        self.assertFalse(form.is_valid())
        self.assertIn('zip_code', form.errors)
