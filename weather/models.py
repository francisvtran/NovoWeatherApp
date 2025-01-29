from django.core.exceptions import ValidationError
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25)
    zip_code = models.CharField(max_length=5, default='00000', unique = True)

    def __str__(self): #show the actual city name on the dashboard
        return self.name
    
    def clean(self):
        #Ensure ZIP code is exactly 5 digits.
        if not self.zip_code.isdigit() or len(self.zip_code) != 5:
            raise ValidationError("ZIP code must be exactly 5 digits.")

    def save(self, *args, **kwargs):
        #Override save method to enforce validation.
        self.full_clean()  # Calls the clean() method before saving
        super().save(*args, **kwargs)

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'