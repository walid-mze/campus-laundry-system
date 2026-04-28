from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [("student", "Student"), ("admin", "Admin")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == "admin"


class Machine(models.Model):
    MACHINE_TYPES = [("washer", "Washer"), ("dryer", "Dryer")]
    STATUS_CHOICES = [("available", "Available"), ("maintenance", "Maintenance")]

    type = models.CharField(max_length=10, choices=MACHINE_TYPES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="available")
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.get_type_display()} #{self.pk} — {self.location}"


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} – {self.end_time.strftime('%H:%M')}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="active")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.user} — {self.machine} on {self.date} [{self.timeslot}]"


class Waitlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="waitlist_entries")
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField()
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user} waiting for {self.machine} on {self.date} [{self.timeslot}]"


class Notification(models.Model):
    TYPE_CHOICES = [
        ("reminder", "Reminder"),
        ("waitlist", "Slot Available"),
        ("cancellation", "Cancellation"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.type}] {self.user} — {self.created_at:%Y-%m-%d %H:%M}"
