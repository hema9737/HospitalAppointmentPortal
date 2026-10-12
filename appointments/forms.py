from django import forms
from .models import Patient, Appointment
from django.utils import timezone


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name',
            'email',
            'phone',
            'date_of_birth',
            'address',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Full name'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email address'}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Phone number'}
            ),
            'address': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time_slot', 'reason']

        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'time_slot': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'reason': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Describe your reason for the visit',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = self.fields[
            'doctor'
        ].queryset.filter(is_active=True)
        self.fields['doctor'].empty_label = "-- Choose a Specialist --"

    def clean_date(self):
        appointment_date = self.cleaned_data.get('date')

        if appointment_date and appointment_date < timezone.localdate():
            raise forms.ValidationError(
                "You cannot book an appointment for a past date."
            )

        return appointment_date