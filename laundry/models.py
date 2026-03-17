from django.db import models
from django.contrib.auth.models import User

class Machine(models.Model):
    MACHINE_TYPES=[("washer","Washer"),("dryer","Dryer")]
    STATUS_CHOICES=[("available","Available"),("maitenance","maintenance")]
    type=models.CharField(max_length=10,choices=MACHINE_TYPES)
    status=models.CharField(max_length=15,choices=STATUS_CHOICES)
    location=models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.type} - {self.location}"

class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

class Booking(models.Model):
    STATUS_CHOICES=[("active","Active"),("cancelled","Cancelled"),("completed","completed")]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    timeslot=models.ForeignKey(TimeSlot,on_delete=models.CASCADE)
    status=models.CharField(max_length=15,choices=STATUS_CHOICES,default="active")
    date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.machine} - {self.timeslot} -{self.date} "
