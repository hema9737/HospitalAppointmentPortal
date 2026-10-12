
from django.db import models
from django.core.validators import MinValueValidator


class Doctor(models.Model):
    DEPARTMENTS = [
        ('Cardiology', 'Cardiology'),
        ('Pediatrics', 'Pediatrics'),
        ('Orthopedics', 'Orthopedics'),
        ('Neurology', 'Neurology'),
    ]

    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    specialization = models.CharField(max_length=100)
    consultation_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    available_days = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    @property
    def display_name(self):
        clean_name = self.name.strip()
        if clean_name.startswith("Dr."):
            clean_name = clean_name[3:].strip()
        elif clean_name.startswith("Dr "):
            clean_name = clean_name[3:].strip()
        return f"Dr. {clean_name}"

    @property
    def image_static_path(self):
        mapping = {
            1: "appointments/images/doctors/doctor_1.jpg",
            2: "appointments/images/doctors/doctor_2.jpg",
            3: "appointments/images/doctors/doctor_3.jpg",
            4: "appointments/images/doctors/doctor_4.jpg",
        }
        return mapping.get(self.id, "appointments/images/doctors/doctor_default.jpg")

    def __str__(self):
        return f"{self.display_name} - {self.specialization}"


class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='appointments'
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='appointments'
    )
    date = models.DateField()
    time_slot = models.TimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date', 'time_slot'],
                name='unique_doctor_appointment_slot'
            )
        ]
        ordering = ['date', 'time_slot']

    def __str__(self):
        return f"{self.patient} - Dr. {self.doctor.name} - {self.date}"


class MedicalReport(models.Model):
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name='reports'
    )
    report_title = models.CharField(max_length=200)
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_title} - {self.appointment.patient.name}"
