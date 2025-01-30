from django.core.exceptions import ValidationError
import datetime
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=25, help_text="Name of this location.")
    zip_code = models.CharField(max_length=5, default='', null=False, blank=True)
    temp_min = models.FloatField(null=True)
    temp_max = models.FloatField(null=True)
    icon = models.CharField(max_length=256, default='', null=False, blank=True)
    date = models.DateField(default=datetime.date.today)

    def __str__(self): #show the actual name of the location on the dashboard
        return self.name
    
    def clean(self):
        #Ensure ZIP code is exactly 5 digits.
        if not self.zip_code.isdigit() or len(self.zip_code) != 5:
            raise ValidationError("ZIP code must be exactly 5 digits.")

    def save(self, *args, **kwargs):
        #Override save method to enforce validation.
        self.full_clean()  # Calls the clean() method before saving
        super().save(*args, **kwargs)