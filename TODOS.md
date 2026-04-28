# Project Task Distribution

## 1. Project Setup (Together)

- [x] Initialize Django project
- [x] Create `laundry` app
- [x] Configure database
- [x] Configure static and templates folders
- [x] Push initial project structure to GitHub

---

# member 1 — Booking & Time Management

## Models

- [x] Create `TimeSlot` model (`start_time`, `end_time`)
- [x] Create `Booking` model (`user`, `machine`, `timeslot`, `status`, `created_at`)

## Booking Logic

- [x] Implement machine booking function
- [x] Implement reservation of washing machines and dryers by time slot
- [x] Prevent double booking of the same machine and timeslot
- [x] Implement booking cancellation
- [x] Implement booking rescheduling
- [x] Implement booking history retrieval for users

## Availability

- [x] Write function to check available machines for a given time
- [x] Write function to check available timeslots for a machine
- [x] Validate slot availability before confirming a booking

## Smart Features

- [x] Implement waitlist if all machines are booked
- [ ] Implement auto-release for unused reservations after a grace period

## Testing

- [x] Test booking conflicts
- [x] Test cancellation and rescheduling
- [x] Test waitlist logic
- [x] Test auto-release logic

---

# member 2 — Users, Machines & Admin

## Authentication

- [x] Implement user registration
- [x] Implement login and logout
- [x] Add user roles (`student` / `admin`)

## Models

- [x] Create `Machine` model (`type: washer/dryer`, `status`, `location`)
- [x] Add maintenance status for machines

## Machine Management

- [x] Implement machine CRUD (add/edit/delete)
- [x] Implement maintenance toggle (`available` / `maintenance`)
- [x] Create endpoint to list all machines
- [x] Implement real-time display of machine availability
- [x] Implement live availability updates

## Admin Features

- [x] Implement admin dashboard logic
- [x] Implement schedule management for machines
- [x] Implement view to see all bookings
- [x] Implement machine usage statistics

## Smart Features

- [x] Implement reminder notifications logic
- [x] Implement analytics for machine usage

## Testing

- [x] Test machine management
- [x] Test user role restrictions
- [x] Test maintenance status behavior
- [x] Test availability updates
- [x] Test reminder logic

---

# Shared Tasks (Together)

## Integration

- [x] Connect machine availability with booking logic
- [x] Connect users with booking system
- [x] Ensure maintenance blocks reservations
- [x] Ensure cancelled or auto-released bookings free the slot
- [x] Test full reservation workflow

## Frontend

- [x] Create machine availability page
- [x] Create booking page
- [x] Display live machine availability in the booking interface
- [x] Create user dashboard
- [x] Create admin dashboard

---

# Finalization

- [x] Write README documentation
- [ ] Add screenshots to GitHub
- [ ] Deploy the application
- [x] Prepare project presentation
