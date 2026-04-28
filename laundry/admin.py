from django.contrib import admin

from .models import Booking, Machine, Notification, TimeSlot, UserProfile, Waitlist


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("__str__", "type", "status", "location")
    list_filter = ("type", "status")
    search_fields = ("location",)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("__str__", "start_time", "end_time")
    ordering = ("start_time",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "machine", "timeslot", "date", "status", "created_at")
    list_filter = ("status", "date")
    search_fields = ("user__username",)
    date_hierarchy = "date"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)


@admin.register(Waitlist)
class WaitlistAdmin(admin.ModelAdmin):
    list_display = ("user", "machine", "timeslot", "date", "notified", "created_at")
    list_filter = ("notified",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "is_read", "created_at")
    list_filter = ("type", "is_read")
