from .models import Booking, Machine, Notification, TimeSlot, Waitlist


def get_available_machines(date, timeslot):
    """Return machines that are available (not under maintenance and not booked) for the given date/timeslot."""
    booked_ids = Booking.objects.filter(
        date=date, timeslot=timeslot, status="active"
    ).values_list("machine_id", flat=True)
    return Machine.objects.filter(status="available").exclude(id__in=booked_ids)


def get_available_timeslots(date, machine):
    """Return timeslots not yet booked for the given machine and date."""
    booked_ids = Booking.objects.filter(
        date=date, machine=machine, status="active"
    ).values_list("timeslot_id", flat=True)
    return TimeSlot.objects.exclude(id__in=booked_ids)


def promote_waitlist(machine, timeslot, booking_date):
    """
    When a slot opens up, notify and promote the first waitlisted user.
    Creates an in-app Notification so they know to book.
    """
    entry = (
        Waitlist.objects.filter(
            machine=machine,
            timeslot=timeslot,
            date=booking_date,
            notified=False,
        )
        .order_by("created_at")
        .first()
    )
    if entry:
        Notification.objects.create(
            user=entry.user,
            type="waitlist",
            message=(
                f"A slot opened up for {machine} on {booking_date} "
                f"[{timeslot}]. Book it before someone else does!"
            ),
        )
        entry.notified = True
        entry.save()
