from django.contrib import admin

# Register your models here.
from .models import Machine, TimeSlot, Booking

admin.site.register(Machine)
admin.site.register(TimeSlot)
admin.site.register(Booking)