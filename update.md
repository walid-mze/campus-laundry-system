
## Implemented Functionalities

### User Management & Authentication
- User registration and login/logout system
- User roles: Student and Admin
- User profiles with role-based access control

### Booking System
- Create booking (machine + date + timeslot)
- Quick booking from machine list (one-click)
- Automatic assignment of logged-in user
- Prevent double booking (same machine, date, timeslot)
- Booking history per user
- Booking cancellation with notifications
- Booking rescheduling with conflict checking

### Availability System
- Only machines with status `available` are selectable
- Real-time availability checking
- Conflict detection before saving booking
- AJAX endpoint for dynamic timeslot availability
- Machine list with grouped display (washers/dryers)

### Waitlist System
- Join waitlist when slots are unavailable
- Automatic promotion when slots open up
- Notifications for waitlist updates
- Waitlist management and tracking

### Notification System
- In-app notifications for various events
- Reminder notifications for upcoming bookings (30 minutes before)
- Waitlist availability notifications
- Cancellation confirmations
- Management command for sending reminders

### Admin Panel
- Admin dashboard with system statistics
- Machine management: CRUD operations (Create, Read, Update, Delete)
- Maintenance mode toggle for machines
- View all bookings across the system
- Analytics: machine usage stats, booking status breakdown, daily trends
- Admin-only access control

### Dashboard
- User dashboard with active bookings
- Upcoming bookings for today
- Recent booking history
- Unread notifications display
- Booking statistics (total, cancelled)

---

## Models

### UserProfile (`laundry/models.py`)
Extends Django User model.

- `user`: OneToOneField to Django User
- `role`: student / admin
- `is_admin`: property for admin check

### Machine (`laundry/models.py`)
Represents a laundry machine.

- `type`: washer / dryer
- `status`: available / maintenance
- `location`: machine location

### TimeSlot (`laundry/models.py`)
Represents a reusable time interval.

- `start_time`
- `end_time`
- Ordering by start_time

### Booking (`laundry/models.py`)
Represents a reservation.

- `user`: linked to Django User
- `machine`: selected machine
- `timeslot`: selected time interval
- `date`: reservation date
- `status`: active / cancelled / completed
- `created_at`: timestamp
- Ordering by date and created_at

### Waitlist (`laundry/models.py`)
Waitlist for unavailable slots.

- `user`: linked to User
- `machine`: linked to Machine
- `timeslot`: linked to TimeSlot
- `date`: booking date
- `notified`: boolean for notification status
- `created_at`: timestamp

### Notification (`laundry/models.py`)
In-app notification system.

- `user`: linked to User
- `type`: reminder / waitlist / cancellation
- `message`: notification text
- `is_read`: read status
- `created_at`: timestamp

---

## Views

### Public Views
- `home`: Display all machines
- `machine_list`: Public machine availability with booking interface
- `ajax_available_timeslots`: AJAX endpoint for timeslot availability

### Authentication Views
- `register_view`: User registration
- `login_view`: User login
- `logout_view`: User logout

### User Dashboard & Booking
- `dashboard`: User dashboard with bookings and notifications
- `create_booking`: Form-based booking creation
- `quick_book`: One-click booking from machine list
- `booking_history`: User's booking history
- `cancel_booking`: Cancel active booking
- `reschedule_booking`: Reschedule existing booking

### Waitlist & Notifications
- `join_waitlist`: Join waitlist for unavailable slot
- `notification_list`: View user notifications

### Admin Views
- `admin_dashboard`: Admin overview with statistics
- `admin_machine_list`: List all machines
- `admin_machine_create`: Add new machine
- `admin_machine_edit`: Edit existing machine
- `admin_machine_delete`: Delete machine
- `admin_toggle_maintenance`: Toggle machine status
- `admin_all_bookings`: View all bookings
- `admin_stats`: Detailed analytics

---

## Forms

### `RegisterForm` (`laundry/forms.py`)
User registration form.

- Based on Django User model
- Includes password confirmation
- Creates UserProfile with default student role

### `BookingForm` (`laundry/forms.py`)
Booking creation form.

- ModelForm based on Booking
- Fields: `machine`, `timeslot`, `date`
- Filters machines to only show available ones
- Custom validation for availability

### `RescheduleForm` (`laundry/forms.py`)
Booking rescheduling form.

- Fields: `date`, `timeslot`, `machine`
- Validates new slot availability

### `MachineForm` (`laundry/forms.py`)
Machine management form.

- ModelForm for Machine model
- All fields included

---

## Utilities

### `get_available_machines(date, timeslot)` (`laundry/utils.py`)
Returns machines available for given date/timeslot.

- Excludes machines under maintenance
- Excludes already booked machines

### `get_available_timeslots(date, machine)` (`laundry/utils.py`)
Returns timeslots available for given machine/date.

- Excludes already booked timeslots

### `promote_waitlist(machine, timeslot, date)` (`laundry/utils.py`)
Handles waitlist promotion when slots open.

- Finds first unnotified waitlist entry
- Creates notification for the user
- Marks entry as notified

---

## Management Commands

### `send_reminders` (`laundry/management/commands/send_reminders.py`)
Automated reminder system.

- Runs every 5 minutes via cron
- Sends notifications for bookings starting within 30 minutes
- Prevents duplicate reminders

---

## Templates

Located in `laundry/templates/laundry/` and `templates/`:

### Public Templates
- `home.html`: Landing page with machine overview
- `machine_list.html`: Interactive machine availability display
- `login.html`: Login form
- `register.html`: Registration form

### User Templates
- `dashboard.html`: User dashboard
- `create_booking.html`: Booking form
- `booking_history.html`: Booking list
- `reschedule_booking.html`: Reschedule form
- `notifications.html`: Notification list

### Admin Templates
- `admin_dashboard.html`: Admin statistics
- `admin_machine_list.html`: Machine management
- `admin_machine_form.html`: Machine add/edit form
- `admin_all_bookings.html`: All bookings view
- `admin_stats.html`: Analytics charts

### Base Templates
- `base.html`: Main layout with navigation

---

## Static Files

Located in `static/`:

- `css/style.css`: Custom styling
- Bootstrap and other assets (assumed via CDN in templates)

---

## URL Configuration

### Main URLs (`config/urls.py`)
- Admin interface
- Laundry app URLs

### App URLs (`laundry/urls.py`)
- Public pages: home, machine_list
- Auth: register, login, logout
- User: dashboard, booking_history, create_booking, etc.
- Admin: admin_dashboard, machine management, stats
- AJAX: available_timeslots

---

## Security & Access Control

- `@login_required` decorators on protected views
- Admin role checking with `_require_admin()` helper
- CSRF protection on forms
- SQL injection prevention via Django ORM
- XSS protection via template escaping

---

## Database

- SQLite for development (configured in settings)
- Migrations in `laundry/migrations/`
- Ready for production database configuration

---

## Future Enhancements

- Auto-release for unused reservations (grace period)
- Email notifications (currently in-app only)
- Real-time updates via WebSockets
- Mobile app API
- Advanced analytics and reporting
- Integration with campus authentication systems  
