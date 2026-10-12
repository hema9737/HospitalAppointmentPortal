from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from appointments.models import Doctor, Patient, Appointment, MedicalReport
from appointments.forms import AppointmentForm, PatientForm


class PortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.doctor1 = Doctor.objects.create(
            name="Dr.Ananya Rao",
            department="Cardiology",
            specialization="Cardiologist",
            consultation_fee=500.00,
            available_days="Monday,Wednesday,Friday",
            is_active=True,
        )
        self.doctor2 = Doctor.objects.create(
            name="Dr.Rahul Sharma",
            department="Pediatrics",
            specialization="Pediatrician",
            consultation_fee=400.00,
            available_days="Tuesday,Thursday,Saturday",
            is_active=True,
        )

    def test_doctor_properties(self):
        # display_name should normalize prefix
        self.assertEqual(self.doctor1.display_name, "Dr. Ananya Rao")
        self.assertEqual(self.doctor2.display_name, "Dr. Rahul Sharma")

        # image_static_path
        self.assertTrue(self.doctor1.image_static_path.startswith("appointments/images/doctors/"))

        # __str__
        self.assertIn("Dr. Ananya Rao - Cardiologist", str(self.doctor1))

    def test_homepage_renders(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/home.html')
        self.assertContains(response, "CarePoint+")
        self.assertContains(response, "Quality Healthcare,")
        self.assertContains(response, "Cardiology")
        self.assertContains(response, "Pediatrics")
        self.assertContains(response, "Orthopedics")
        self.assertContains(response, "Neurology")
        self.assertContains(response, "Dr. Ananya Rao")
        self.assertContains(response, "500.00")
        self.assertContains(response, "Book Appointment")

    def test_booking_page_renders_and_preselects_doctor(self):
        response = self.client.get(reverse('book_appointment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/book_appointment.html')

        # Test preselection with query parameter
        response_with_doctor = self.client.get(
            f"{reverse('book_appointment')}?doctor={self.doctor1.id}"
        )
        self.assertEqual(response_with_doctor.status_code, 200)
        # Check initial doctor in form context
        form = response_with_doctor.context['appointment_form']
        self.assertEqual(form.initial.get('doctor'), self.doctor1.id)

    def test_successful_booking_submission(self):
        future_date = date.today() + timedelta(days=5)
        post_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '9876543210',
            'date_of_birth': '1990-01-01',
            'address': '123 Main Street',
            'doctor': self.doctor1.id,
            'date': future_date.strftime('%Y-%m-%d'),
            'time_slot': '10:00:00',
            'reason': 'Routine health checkup',
        }
        response = self.client.post(reverse('book_appointment'), data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your appointment request has been submitted successfully!')

        # Verify in database
        patient = Patient.objects.filter(email='john.doe@example.com').first()
        self.assertIsNotNone(patient)
        appointment = Appointment.objects.filter(patient=patient, doctor=self.doctor1).first()
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.status, 'Pending')

    def test_past_date_validation_rejected(self):
        past_date = date.today() - timedelta(days=2)
        post_data = {
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'phone': '9876543211',
            'date_of_birth': '1992-05-15',
            'address': '456 Second Ave',
            'doctor': self.doctor1.id,
            'date': past_date.strftime('%Y-%m-%d'),
            'time_slot': '11:00:00',
            'reason': 'Consultation',
        }
        response = self.client.post(reverse('book_appointment'), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You cannot book an appointment for a past date.')

    def test_duplicate_slot_handled_gracefully(self):
        target_date = date.today() + timedelta(days=7)
        # First booking
        patient1 = Patient.objects.create(
            name="Alice",
            email="alice@example.com",
            phone="1111111111"
        )
        Appointment.objects.create(
            patient=patient1,
            doctor=self.doctor1,
            date=target_date,
            time_slot="14:00:00",
            reason="Checkup"
        )

        # Attempt second booking for the same doctor, date, and time
        duplicate_data = {
            'name': 'Bob',
            'email': 'bob@example.com',
            'phone': '2222222222',
            'doctor': self.doctor1.id,
            'date': target_date.strftime('%Y-%m-%d'),
            'time_slot': '14:00:00',
            'reason': 'Second consultation attempt',
        }
        response = self.client.post(reverse('book_appointment'), data=duplicate_data)
        self.assertEqual(response.status_code, 200)
        # Unique constraint is caught by ModelForm validation or database IntegrityError
        has_duplicate_error = (
            "Appointment with this Doctor, Date and Time slot already exists." in response.content.decode()
            or "This doctor already has an appointment at that date and time" in response.content.decode()
        )
        self.assertTrue(has_duplicate_error)
