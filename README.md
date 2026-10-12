# Hospital Appointment Portal 🏥

A modern, responsive web application for managing doctor appointments and patient consultations built with Django.

## ✨ Features

- **Doctor Directory & Profiles**: Browse certified medical specialists categorized by departments (Cardiology, Pediatrics, Orthopedics, Neurology) with consultation fees and availability schedules.
- **Appointment Booking**: Intuitive booking workflow with real-time validation, date selection, and duplicate slot prevention.
- **Patient Management**: Automated patient profile handling and appointment history tracking.
- **Responsive Healthcare UI**: Modern medical-themed design optimized for desktop and mobile devices.
- **Django Admin Integration**: Comprehensive backend dashboard to manage doctors, patients, appointments, and medical reports.

## 🛠️ Tech Stack

- **Backend**: Python 3, Django 5.2
- **Frontend**: HTML5, CSS3 (Custom Responsive Medical UI)
- **Database**: SQLite (Development / Production ready for PostgreSQL)
- **Static Files**: Django Staticfiles & WhiteNoise

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/hema9737/HospitalAppointmentPortal.git
cd HospitalAppointmentPortal
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Load Initial Data
```bash
python manage.py migrate
python manage.py loaddata appointments/fixtures/initial_data.json
```

### 5. Create Superuser (Optional for Admin Access)
```bash
python manage.py createsuperuser
```

### 6. Start the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

## 📁 Project Structure

```
HospitalAppointmentPortal/
├── appointments/               # Appointments application
│   ├── fixtures/               # Seed data for doctors and appointments
│   ├── migrations/             # Database migrations
│   ├── static/appointments/    # CSS styles and doctor images
│   ├── templates/appointments/ # HTML templates (home, book_appointment)
│   ├── admin.py                # Admin portal configurations
│   ├── forms.py                # Form validations
│   ├── models.py               # Doctor, Patient, Appointment models
│   ├── urls.py                 # App routing
│   └── views.py                # View controllers
├── hospital_project/           # Project configuration & settings
├── db.sqlite3                  # Local database
├── manage.py                   # Django CLI entrypoint
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```
