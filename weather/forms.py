from django import forms
from django.forms import ModelForm, TextInput
import datetime
from weather.models.location import Location


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['zip_code']
        widgets = {
            'zip_code': TextInput(attrs={'class' : 'input', 'placeholder' : 'Enter Valid U.S. ZIP Code'}),
        } 

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['zip_code'].initial = ''

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')

        #Validates 5-digit ZIP code
        if not zip_code.isdigit() or len(zip_code) != 5:
            raise forms.ValidationError("Enter a valid 5-digit U.S. ZIP Code.")
        
        if Location.objects.filter(zip_code=zip_code, date=datetime.date.today()).exists():
            raise forms.ValidationError("This ZIP Code is already added.")
    
        return zip_code