# Campus Laundry System

A comprehensive web application built with Django that allows students to view machine availability and book laundry time slots, while enabling administrators to manage machines and schedules efficiently.

## Features

### For Students
- **User Registration & Authentication**: Secure login system with student/admin roles
- **Machine Availability View**: Real-time display of available washers and dryers with collapsible time slots
- **Booking System**: Easy booking of machines for specific dates and time slots
- **Quick Booking**: One-click booking directly from the machine list
- **Booking Management**: View booking history, cancel bookings, and reschedule existing bookings
- **Waitlist**: Join waitlists for unavailable slots and get notified when they open up
- **Notifications**: In-app notifications for reminders, waitlist updates, and booking confirmations
- **Dashboard**: Personalized dashboard showing active bookings, upcoming slots, recent activity, and notifications

### For Administrators
- **Admin Dashboard**: Overview of system statistics including total machines, bookings, and waitlist counts
- **Machine Management**: Full CRUD operations for machines (add, edit, delete)
- **Maintenance Mode**: Toggle machines between available and maintenance status
- **Booking Oversight**: View all bookings across the system
- **Analytics**: Detailed statistics on machine usage, booking status breakdown, and daily booking trends
- **User Management**: Access to all user accounts and their booking history

### Smart Features
- **Conflict Prevention**: Automatic detection and prevention of double bookings
- **Waitlist System**: Automatic promotion of waitlisted users when slots become available
- **Reminder System**: Automated notifications for bookings starting within 30 minutes
- **Real-time Availability**: Live updates of machine and slot availability

## Technology Stack

- **Backend**: Django 5.2.11
- **Database**: SQLite (development), configurable for production
- **Frontend**: HTML, CSS, Bootstrap (via templates)
- **Authentication**: Django's built-in auth system with custom user profiles

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd campus-laundry-system
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Admin interface: `http://127.0.0.1:8000/admin/`

### Setting up Reminder Notifications

To enable automated reminder notifications, set up a cron job to run the reminder command every 5 minutes:

```bash
# Add to crontab (crontab -e)
*/5 * * * * /path/to/venv/bin/python /path/to/campus-laundry-system/manage.py send_reminders
```

## Usage

### For Students
1. Register an account or log in
2. View available machines on the home page or machine list
3. Book a machine by selecting a date and time slot
4. Manage your bookings from the dashboard or booking history
5. Receive notifications for reminders and waitlist updates

### For Administrators
1. Log in with admin credentials
2. Access the admin dashboard for system overview
3. Manage machines through the admin interface
4. View all bookings and user statistics
5. Toggle machine maintenance status as needed

## Project Structure

```
campus-laundry-system/
├── config/                 # Django project settings
├── laundry/                # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── utils.py           # Utility functions
│   ├── management/        # Django management commands
│   └── templates/         # HTML templates
├── static/                # Static files (CSS, JS)
├── templates/             # Base templates
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Models

- **UserProfile**: Extends Django User with role (student/admin)
- **Machine**: Represents laundry machines with type, status, and location
- **TimeSlot**: Defines available time intervals
- **Booking**: User reservations with status tracking
- **Waitlist**: Queue system for unavailable slots
- **Notification**: In-app notification system

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
