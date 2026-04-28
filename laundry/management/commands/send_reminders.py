"""
Management command: send_reminders

Creates in-app reminder notifications for users whose active booking starts
within the next 30 minutes and who have not yet been reminded.

Usage:
    python manage.py send_reminders

Schedule via cron to run every 5 minutes:
    */5 * * * * /path/to/venv/bin/python /path/to/manage.py send_reminders
"""

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from laundry.models import Booking, Notification


REMINDER_WINDOW_MINUTES = 30


class Command(BaseCommand):
    help = "Send reminder notifications for bookings starting within 30 minutes."

    def handle(self, *args, **options):
        now = timezone.now()
        today = now.date()
        reminded = 0

        active_bookings = Booking.objects.filter(
            status="active", date=today
        ).select_related("machine", "timeslot", "user")

        for booking in active_bookings:
            slot_start = datetime.combine(booking.date, booking.timeslot.start_time)
            if timezone.is_naive(slot_start):
                slot_start = timezone.make_aware(slot_start)

            time_until = slot_start - now
            if timedelta(0) <= time_until <= timedelta(minutes=REMINDER_WINDOW_MINUTES):
                # Avoid duplicate reminders by checking both slot and date in the message
                already_reminded = Notification.objects.filter(
                    user=booking.user,
                    type="reminder",
                    message__icontains=str(booking.date),
                ).filter(
                    message__icontains=str(booking.timeslot),
                ).exists()

                if not already_reminded:
                    minutes_away = int(time_until.total_seconds() / 60)
                    Notification.objects.create(
                        user=booking.user,
                        type="reminder",
                        message=(
                            f"Reminder: your booking for {booking.machine} starts in "
                            f"~{minutes_away} minute(s) [{booking.timeslot}] on {booking.date}."
                        ),
                    )
                    reminded += 1

        self.stdout.write(self.style.SUCCESS(f"Sent {reminded} reminder(s)."))
