from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking 

# Create your views here.
@login_required
def create_booking(request):
    if request.method=="POST":
        form=BookingForm(request.POST)
        if form.is_valid():
            booking=form.save(commit=False)
            form = BookingForm(request.POST)
            exists = Booking.objects.filter(
                machine=booking.machine,
                timeslot=booking.timeslot,
                date=booking.date,
                status="active"
            ).exists()
            if exists:
                form.add_error(None,"this machine is already booked for that date and time slot.")
            else:
                form.save()
                return redirect("booking_history")
    else:
        form=BookingForm()
    return render(request, "laundry/create_booking.html", {"form": form})
    
    
@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-date", "-created_at")
    return render(request, "laundry/booking_history.html", {"bookings": bookings})

