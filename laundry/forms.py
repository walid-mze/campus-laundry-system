from django import forms 
from django import forms
from .models import Booking, Machine, TimeSlot

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["machine", "timeslot", "date"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["machine"].queryset = Machine.objects.filter(status="available")