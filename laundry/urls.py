from django.urls import path
from . import views

urlpatterns = [
    path("book/", views.create_booking, name="create_booking"),
    path("history/", views.booking_history, name="booking_history"),
]