# Project Task Distribution

## 1. Project Setup (Together)

- [ ] Initialize Django project
- [ ] Create `laundry` app
- [ ] Configure database
- [ ] Configure static and templates folders
- [ ] Push initial project structure to GitHub

---

# member 1 — Booking & Time Management

## Models

- [ ] Create `TimeSlot` model (`start_time`, `end_time`)
- [ ] Create `Booking` model (`user`, `machine`, `timeslot`, `status`, `created_at`)

## Booking Logic

- [ ] Implement machine booking function
- [ ] Implement reservation of washing machines and dryers by time slot
- [ ] Prevent double booking of the same machine and timeslot
- [ ] Implement booking cancellation
- [ ] Implement booking rescheduling
- [ ] Implement booking history retrieval for users

## Availability

- [ ] Write function to check available machines for a given time
- [ ] Write function to check available timeslots for a machine
- [ ] Validate slot availability before confirming a booking

## Smart Features

- [ ] Implement waitlist if all machines are booked
- [ ] Implement auto-release for unused reservations after a grace period

## Testing

- [ ] Test booking conflicts
- [ ] Test cancellation and rescheduling
- [ ] Test waitlist logic
- [ ] Test auto-release logic

---

# member 2 — Users, Machines & Admin

## Authentication

- [ ] Implement user registration
- [ ] Implement login and logout
- [ ] Add user roles (`student` / `admin`)

## Models

- [ ] Create `Machine` model (`type: washer/dryer`, `status`, `location`)
- [ ] Add maintenance status for machines

## Machine Management

- [ ] Implement machine CRUD (add/edit/delete)
- [ ] Implement maintenance toggle (`available` / `unavailable`)
- [ ] Create endpoint to list all machines
- [ ] Implement real-time display of machine availability
- [ ] Implement live availability updates

## Admin Features

- [ ] Implement admin dashboard logic
- [ ] Implement schedule management for machines
- [ ] Implement view to see all bookings
- [ ] Implement machine usage statistics

## Smart Features

- [ ] Implement reminder notifications logic
- [ ] Implement analytics for machine usage

## Testing

- [ ] Test machine management
- [ ] Test user role restrictions
- [ ] Test maintenance status behavior
- [ ] Test availability updates
- [ ] Test reminder logic

---

# Shared Tasks (Together)

## Integration

- [ ] Connect machine availability with booking logic
- [ ] Connect users with booking system
- [ ] Ensure maintenance blocks reservations
- [ ] Ensure cancelled or auto-released bookings free the slot
- [ ] Test full reservation workflow

## Frontend

- [ ] Create machine availability page
- [ ] Create booking page
- [ ] Display live machine availability in the booking interface
- [ ] Create user dashboard
- [ ] Create admin dashboard

---

# Finalization

- [ ] Write README documentation
- [ ] Add screenshots to GitHub
- [ ] Deploy the application
- [ ] Prepare project presentation