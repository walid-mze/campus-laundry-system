from .models import Machine, Booking, TimeSlot


def get_available_machines(date, timeslot):
    booked_machine_ids = Booking.objects.filter(
        date=date,
        timeslot=timeslot,
        status="active"
    ).values_list("machine_id", flat=True)

    return Machine.objects.filter(status="available").exclude(id__in=booked_machine_ids)


def get_available_timeslots(date, machine):
    booked_timeslot_ids = Booking.objects.filter(
        date=date,
        machine=machine,
        status="active"
    ).values_list("timeslot_id", flat=True)

    return TimeSlot.objects.exclude(id__in=booked_timeslot_ids)