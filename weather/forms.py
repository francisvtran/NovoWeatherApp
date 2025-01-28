from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['zip_code']
        widgets = {
            'zip_code': TextInput(attrs={'class' : 'input', 'placeholder' : 'Enter ZIP Code'}),
        } 