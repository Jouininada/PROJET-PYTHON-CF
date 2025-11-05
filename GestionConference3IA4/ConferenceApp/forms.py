from django import forms
from .models import Conference

class ConferenceModel(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'theme', 'description', 'location', 'start_date', 'end_date']  
        labels = {
            'name': "Nom de la conférence",
            'theme': "Thème de la conférence",
            'description': 'Description',
            'location': 'Lieu de la conférence',
            'start_date': 'Date de début',
            'end_date': "Date de fin"
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': "Ex : Conférence 3IA4"
                }
            ),
            "start_date": forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': "Date de début"
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': "Date de fin"
                }
            ),
        }
