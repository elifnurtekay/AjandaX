from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'start_time', 'end_time', 'location']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }),
        }


"""class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'start_time', 'end_time', 'location']
"""