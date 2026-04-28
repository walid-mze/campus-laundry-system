from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Booking, Machine, TimeSlot


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "min": str(date.today())}))

    class Meta:
        model = Booking
        fields = ["machine", "timeslot", "date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["machine"].queryset = Machine.objects.filter(status="available")

    def clean_date(self):
        selected = self.cleaned_data["date"]
        if selected < date.today():
            raise forms.ValidationError("You cannot book a date in the past.")
        return selected


class RescheduleForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "min": str(date.today())}))
    machine = forms.ModelChoiceField(queryset=Machine.objects.filter(status="available"))
    timeslot = forms.ModelChoiceField(queryset=TimeSlot.objects.all())

    def clean_date(self):
        selected = self.cleaned_data["date"]
        if selected < date.today():
            raise forms.ValidationError("You cannot reschedule to a date in the past.")
        return selected


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ["type", "status", "location"]
