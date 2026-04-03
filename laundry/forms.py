from django import forms 
from django import forms
from .models import Booking, Machine, TimeSlot

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["machine", "timeslot", "date"]
    def __init__(self, *args, **kwargs):
        available_machines = kwargs.pop("available_machines", None)
        super().__init__(*args, **kwargs)
        if available_machines: 
            self.fields["machine"].queryset = available_machines
        else:
            self.fields["machine"].queryset = Machine.objects.filter(status="available")
