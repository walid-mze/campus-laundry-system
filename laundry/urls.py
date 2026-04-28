from django.urls import path

from . import views

urlpatterns = [
    # Public
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("machines/", views.machine_list, name="machine_list"),

    # Auth
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Booking
    path("book/", views.create_booking, name="create_booking"),
    path("quick-book/", views.quick_book, name="quick_book"),
    path("history/", views.booking_history, name="booking_history"),
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("reschedule/<int:booking_id>/", views.reschedule_booking, name="reschedule_booking"),

    # AJAX
    path("ajax/timeslots/", views.ajax_available_timeslots, name="ajax_available_timeslots"),

    # Waitlist
    path(
        "waitlist/<int:machine_id>/<int:timeslot_id>/<str:booking_date>/",
        views.join_waitlist,
        name="join_waitlist",
    ),

    # Notifications
    path("notifications/", views.notification_list, name="notification_list"),

    # Admin panel
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-panel/machines/", views.admin_machine_list, name="admin_machine_list"),
    path("admin-panel/machines/add/", views.admin_machine_create, name="admin_machine_create"),
    path("admin-panel/machines/<int:machine_id>/edit/", views.admin_machine_edit, name="admin_machine_edit"),
    path("admin-panel/machines/<int:machine_id>/delete/", views.admin_machine_delete, name="admin_machine_delete"),
    path("admin-panel/machines/<int:machine_id>/toggle/", views.admin_toggle_maintenance, name="admin_toggle_maintenance"),
    path("admin-panel/bookings/", views.admin_all_bookings, name="admin_all_bookings"),
    path("admin-panel/stats/", views.admin_stats, name="admin_stats"),
]
