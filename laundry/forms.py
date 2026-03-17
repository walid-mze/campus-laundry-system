from django import forms 
from django import forms
from .models import Booking, Machine, TimeSlot

class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        fields=["machine","timeslot","date"]
        
