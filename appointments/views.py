from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError, transaction
from .models import Doctor, Patient, Appointment
from .forms import PatientForm, AppointmentForm


def home(request):
    doctors = Doctor.objects.filter(is_active=True)
    return render(request, "appointments/home.html", {
        "doctors": doctors,
    })


def book_appointment(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        appointment_form = AppointmentForm(request.POST)

        if patient_form.is_valid() and appointment_form.is_valid():
            try:
                with transaction.atomic():
                    patient_data = patient_form.cleaned_data

                    # Reuse an existing patient with this email.
                    patient = Patient.objects.filter(
                        email=patient_data['email']
                    ).first()

                    if patient:
                        for field in ['name', 'phone', 'date_of_birth', 'address']:
                            setattr(patient, field, patient_data[field])
                        patient.save()
                    else:
                        patient = patient_form.save()

                    appointment = appointment_form.save(commit=False)
                    appointment.patient = patient
                    appointment.save()

                messages.success(
                    request,
                    'Your appointment request has been submitted successfully!'
                )
                return redirect('book_appointment')

            except IntegrityError:
                messages.error(
                    request,
                    'This doctor already has an appointment at that date and time. '
                    'Please select another slot.'
                )
    else:
        # Pre-select doctor if doctor ID is passed in query parameters e.g. ?doctor=1
        initial_appointment = {}
        doctor_id = request.GET.get('doctor')
        if doctor_id:
            try:
                doctor_id = int(doctor_id)
                if Doctor.objects.filter(id=doctor_id, is_active=True).exists():
                    initial_appointment['doctor'] = doctor_id
            except (ValueError, TypeError):
                pass

        patient_form = PatientForm()
        appointment_form = AppointmentForm(initial=initial_appointment)

    return render(
        request,
        'appointments/book_appointment.html',
        {
            'patient_form': patient_form,
            'appointment_form': appointment_form,
        }
    )

