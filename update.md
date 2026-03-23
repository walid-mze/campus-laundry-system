
## Implemented Functionalities

### Booking System
- Create booking (machine + date + timeslot)
- Automatic assignment of logged-in user
- Prevent double booking (same machine, date, timeslot)
- Booking history per user

### Availability (Basic)
- Only machines with status `available` are selectable
- Conflict detection before saving booking

### Authentication (Partial)
- Booking is restricted to logged-in users (`@login_required`)

### Admin Panel
- Manage Machines, TimeSlots, and Bookings via Django admin

---

## Models

### Machine (`laundry/models.py`)
Represents a laundry machine.

- `type`: washer / dryer  
- `status`: available / maintenance  
- `location`: machine location  

---

### TimeSlot (`laundry/models.py`)
Represents a reusable time interval.

- `start_time`  
- `end_time`  

---

### Booking (`laundry/models.py`)
Represents a reservation.

- `user`: linked to Django User  
- `machine`: selected machine  
- `timeslot`: selected time interval  
- `date`: reservation date  
- `status`: active / cancelled / completed  
- `created_at`: timestamp  

---

## Views

### `create_booking` (`laundry/views.py`)
- Displays booking form
- Handles booking submission
- Prevents double booking
- Saves booking if valid
- Redirects to booking history

---

### `booking_history` (`laundry/views.py`)
- Displays all bookings of the logged-in user
- Orders bookings by most recent

---

## Forms

### `BookingForm` (`laundry/forms.py`)
- ModelForm based on Booking
- Fields: `machine`, `timeslot`, `date`
- Filters machines to only show available ones

---

## Templates

Located in `laundry/templates/laundry/`:

- `create_booking.html` → booking form page  
- `booking_history.html` → user bookings list  
