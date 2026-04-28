import json
from datetime import date, datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import BookingForm, MachineForm, RegisterForm, RescheduleForm
from .models import Booking, Machine, Notification, TimeSlot, UserProfile, Waitlist
from .utils import get_available_machines, get_available_timeslots, promote_waitlist


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _require_admin(request):
    """Return True when the request user is a campus admin."""
    return (
        request.user.is_authenticated
        and hasattr(request.user, "profile")
        and request.user.profile.is_admin
    )


# ---------------------------------------------------------------------------
# Public / Home
# ---------------------------------------------------------------------------

def home(request):
    machines = Machine.objects.all()
    return render(request, "laundry/home.html", {"machines": machines})


@login_required
def dashboard(request):
    today = date.today()
    active_bookings   = Booking.objects.filter(user=request.user, status="active").order_by("date", "timeslot__start_time")
    upcoming_today    = active_bookings.filter(date=today)
    recent_bookings   = Booking.objects.filter(user=request.user).order_by("-created_at")[:5]
    waitlist_entries  = request.user.waitlist_entries.filter(notified=False).order_by("date", "timeslot__start_time")
    unread_notifs     = request.user.notifications.filter(is_read=False).order_by("-created_at")[:5]
    total_bookings    = Booking.objects.filter(user=request.user).count()
    cancelled_bookings= Booking.objects.filter(user=request.user, status="cancelled").count()

    return render(request, "laundry/dashboard.html", {
        "today": today,
        "active_bookings": active_bookings,
        "upcoming_today": upcoming_today,
        "recent_bookings": recent_bookings,
        "waitlist_entries": waitlist_entries,
        "unread_notifs": unread_notifs,
        "total_bookings": total_bookings,
        "cancelled_bookings": cancelled_bookings,
    })


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created! Welcome.")
        return redirect("home")
    return render(request, "laundry/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get("next", "home"))
        messages.error(request, "Invalid username or password.")
    return render(request, "laundry/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------------------------------------------------------------------
# Machine Availability
# ---------------------------------------------------------------------------

def machine_list(request):
    """Public page showing machines grouped by type with collapsible time slots."""
    today = date.today()
    machines = Machine.objects.all()
    timeslots = TimeSlot.objects.all()

    booked_qs = Booking.objects.filter(date=today, status="active").values("machine_id", "timeslot_id", "user_id")
    booked_pairs = {(b["machine_id"], b["timeslot_id"]) for b in booked_qs}
    my_pairs = {
        (b["machine_id"], b["timeslot_id"])
        for b in booked_qs
        if request.user.is_authenticated and b["user_id"] == request.user.id
    }

    def build_machine_data(qs):
        result = []
        for m in qs:
            slots = [
                {
                    "timeslot": ts,
                    "is_booked": (m.id, ts.id) in booked_pairs,
                    "is_mine": (m.id, ts.id) in my_pairs,
                }
                for ts in timeslots
            ]
            free_count = sum(1 for s in slots if not s["is_booked"])
            result.append({"machine": m, "slots": slots, "free_count": free_count, "total_count": len(slots)})
        return result

    grouped_machines = [
        ("Washers", "bi-moisture", build_machine_data(machines.filter(type="washer"))),
        ("Dryers",  "bi-wind",     build_machine_data(machines.filter(type="dryer"))),
    ]
    # Only include groups that have at least one machine
    grouped_machines = [(label, icon, items) for label, icon, items in grouped_machines if items]

    return render(request, "laundry/machine_list.html", {
        "grouped_machines": grouped_machines,
        "today": today,
    })


# ---------------------------------------------------------------------------
# AJAX endpoint — available timeslots for a machine on a date
# ---------------------------------------------------------------------------

def ajax_available_timeslots(request):
    machine_id = request.GET.get("machine_id")
    booking_date = request.GET.get("date")
    exclude_booking_id = request.GET.get("exclude_booking_id")  # used during reschedule

    if not machine_id or not booking_date:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    try:
        machine = Machine.objects.get(pk=machine_id)
        parsed_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
    except (Machine.DoesNotExist, ValueError):
        return JsonResponse({"error": "Invalid parameters"}, status=400)

    booked_ids = Booking.objects.filter(
        date=parsed_date,
        machine=machine,
        status="active",
    )
    if exclude_booking_id:
        booked_ids = booked_ids.exclude(pk=exclude_booking_id)
    booked_ids = booked_ids.values_list("timeslot_id", flat=True)

    available = TimeSlot.objects.exclude(id__in=booked_ids)
    data = [{"id": ts.id, "label": str(ts)} for ts in available]
    return JsonResponse({"timeslots": data})


# ---------------------------------------------------------------------------
# Booking
# ---------------------------------------------------------------------------

@login_required
@require_POST
def quick_book(request):
    """One-click booking from the machine list — no form, straight to confirm."""
    from datetime import datetime as dt
    machine_id  = request.POST.get("machine_id")
    timeslot_id = request.POST.get("timeslot_id")
    booking_date = request.POST.get("date")

    try:
        machine  = Machine.objects.get(pk=machine_id)
        timeslot = TimeSlot.objects.get(pk=timeslot_id)
        parsed_date = dt.strptime(booking_date, "%Y-%m-%d").date()
    except (Machine.DoesNotExist, TimeSlot.DoesNotExist, ValueError):
        messages.error(request, "Invalid booking details.")
        return redirect("machine_list")

    from datetime import date as _date
    if parsed_date < _date.today():
        messages.error(request, "Cannot book a date in the past.")
        return redirect("machine_list")

    available = get_available_machines(parsed_date, timeslot)
    if machine not in available:
        messages.error(request, f"{machine} is already booked for {timeslot} on {parsed_date}.")
        return redirect("machine_list")

    Booking.objects.create(
        user=request.user,
        machine=machine,
        timeslot=timeslot,
        date=parsed_date,
    )
    messages.success(request, f"Booked — {machine}, {parsed_date}, {timeslot}.")
    return redirect("booking_history")


@login_required
def create_booking(request):
    waitlist_suggestion = None  # populated when the chosen slot is already taken

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            available = get_available_machines(booking.date, booking.timeslot)
            if booking.machine not in available:
                form.add_error(None, "This machine is already booked for that slot.")
                # Offer to join the waitlist for this exact slot
                waitlist_suggestion = {
                    "machine_id": booking.machine.pk,
                    "timeslot_id": booking.timeslot.pk,
                    "date": booking.date,
                }
            else:
                booking.save()
                messages.success(request, "Booking confirmed!")
                return redirect("booking_history")
    else:
        form = BookingForm()
    return render(request, "laundry/create_booking.html", {
        "form": form,
        "waitlist_suggestion": waitlist_suggestion,
    })


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "laundry/booking_history.html", {"bookings": bookings})


@login_required
@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if booking.status != "active":
        messages.error(request, "Only active bookings can be cancelled.")
        return redirect("booking_history")

    booking.status = "cancelled"
    booking.save()

    # Persistent confirmation notification for the user who cancelled
    Notification.objects.create(
        user=request.user,
        type="cancellation",
        message=(
            f"Your booking for {booking.machine} on {booking.date} "
            f"[{booking.timeslot}] has been successfully cancelled."
        ),
    )

    # Notify + promote first person on the waitlist for that slot
    promote_waitlist(booking.machine, booking.timeslot, booking.date)

    messages.success(request, "Booking cancelled.")
    return redirect("booking_history")


@login_required
def reschedule_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if booking.status != "active":
        messages.error(request, "Only active bookings can be rescheduled.")
        return redirect("booking_history")

    if request.method == "POST":
        form = RescheduleForm(request.POST)
        if form.is_valid():
            new_date = form.cleaned_data["date"]
            new_timeslot = form.cleaned_data["timeslot"]
            new_machine = form.cleaned_data["machine"]

            available = get_available_machines(new_date, new_timeslot)
            if new_machine not in available:
                form.add_error(None, "That slot is not available.")
            else:
                old_machine = booking.machine
                old_timeslot = booking.timeslot
                old_date = booking.date

                booking.date = new_date
                booking.timeslot = new_timeslot
                booking.machine = new_machine
                booking.save()

                # Free the old slot → promote waitlist
                promote_waitlist(old_machine, old_timeslot, old_date)
                messages.success(request, "Booking rescheduled!")
                return redirect("booking_history")
    else:
        form = RescheduleForm(initial={
            "date": booking.date,
            "timeslot": booking.timeslot,
            "machine": booking.machine,
        })

    return render(request, "laundry/reschedule_booking.html", {
        "form": form,
        "booking": booking,
    })


# ---------------------------------------------------------------------------
# Waitlist
# ---------------------------------------------------------------------------

@login_required
@require_POST
def join_waitlist(request, machine_id, timeslot_id, booking_date):
    machine = get_object_or_404(Machine, pk=machine_id)
    timeslot = get_object_or_404(TimeSlot, pk=timeslot_id)

    try:
        parsed_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
    except ValueError:
        messages.error(request, "Invalid date.")
        return redirect("machine_list")

    already = Waitlist.objects.filter(
        user=request.user, machine=machine, timeslot=timeslot, date=parsed_date
    ).exists()

    if already:
        messages.info(request, "You are already on the waitlist for this slot.")
    else:
        Waitlist.objects.create(
            user=request.user, machine=machine, timeslot=timeslot, date=parsed_date
        )
        # Confirm to the user that they will be notified
        Notification.objects.create(
            user=request.user,
            type="waitlist",
            message=(
                f"You joined the waitlist for {machine} on {parsed_date} [{timeslot}]. "
                f"You'll receive a notification here as soon as the slot opens up."
            ),
        )
        messages.success(request, "You're on the waitlist! We'll notify you when the slot opens.")

    return redirect("machine_list")


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------

@login_required
def notification_list(request):
    notifs = Notification.objects.filter(user=request.user)
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, "laundry/notifications.html", {"notifications": notifs})


# ---------------------------------------------------------------------------
# Admin Panel
# ---------------------------------------------------------------------------

@login_required
def admin_dashboard(request):
    if not _require_admin(request):
        messages.error(request, "Access denied.")
        return redirect("home")

    total_machines = Machine.objects.count()
    available_machines = Machine.objects.filter(status="available").count()
    total_bookings = Booking.objects.count()
    active_bookings = Booking.objects.filter(status="active").count()
    pending_waitlist = Waitlist.objects.count()
    recent_bookings = Booking.objects.select_related("user", "machine", "timeslot").order_by("-created_at")[:10]

    return render(request, "laundry/admin_dashboard.html", {
        "total_machines": total_machines,
        "available_machines": available_machines,
        "total_bookings": total_bookings,
        "active_bookings": active_bookings,
        "pending_waitlist": pending_waitlist,
        "recent_bookings": recent_bookings,
    })


@login_required
def admin_machine_list(request):
    if not _require_admin(request):
        messages.error(request, "Access denied.")
        return redirect("home")
    machines = Machine.objects.all()
    return render(request, "laundry/admin_machine_list.html", {"machines": machines})


@login_required
def admin_machine_create(request):
    if not _require_admin(request):
        messages.error(request, "Access denied.")
        return redirect("home")
    form = MachineForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Machine added.")
        return redirect("admin_machine_list")
    return render(request, "laundry/admin_machine_form.html", {"form": form, "action": "Add"})


@login_required
def admin_machine_edit(request, machine_id):
    if not _require_admin(request):
        messages.error(request, "Access denied.")
        return redirect("home")
    machine = get_object_or_404(Machine, pk=machine_id)
    form = MachineForm(request.POST or None, instance=machine)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Machine updated.")
        return redirect("admin_machine_list")
    return render(request, "laundry/admin_machine_form.html", {"form": form, "action": "Edit", "machine": machine})


@login_required
@require_POST
def admin_machine_delete(request, machine_id):
    if not _require_admin(request):
        messages.error(request, "Access denied.")
        return redirect("home")
    machine = get_object_or_404(Machine, pk=machine_id)
    machine.delete()
    messages.success(request, "Machine deleted.")
    return redirect("admin_machine_list")


@login_required
@require_POST
def admin_toggle_maintenance(request, machine_id):
    if not _require_admin(request):
        messages.error(request, "Access denied.")
        return redirect("home")
    machine = get_object_or_404(Machine, pk=machine_id)
    machine.status = "maintenance" if machine.status == "available" else "available"
    machine.save()
    messages.success(request, f"Machine is now {machine.get_status_display()}.")
    return redirect("admin_machine_list")


@login_required
def admin_all_bookings(request):
    if not _require_admin(request):
        messages.error(request, "Access denied.")
        return redirect("home")
    bookings = Booking.objects.select_related("user", "machine", "timeslot").order_by("-date", "-created_at")
    return render(request, "laundry/admin_all_bookings.html", {"bookings": bookings})


@login_required
def admin_stats(request):
    if not _require_admin(request):
        messages.error(request, "Access denied.")
        return redirect("home")

    # Bookings per machine
    machine_usage = (
        Booking.objects.values("machine__type", "machine__location", "machine_id")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    # Bookings per status
    status_breakdown = (
        Booking.objects.values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )
    # Bookings per day (last 14 days)
    from django.db.models.functions import TruncDate
    daily = (
        Booking.objects.annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )

    return render(request, "laundry/admin_stats.html", {
        "machine_usage": machine_usage,
        "status_breakdown": status_breakdown,
        "daily": daily,
    })
