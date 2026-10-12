import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hospital_project.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command
from appointments.models import Doctor

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@hospital.local")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully.")
else:
    print(f"Superuser '{username}' already exists.")

# Ensure initial fixture data is loaded if doctor records are empty
try:
    if Doctor.objects.count() == 0:
        fixture_path = os.path.join("appointments", "fixtures", "initial_data.json")
        if os.path.exists(fixture_path):
            call_command("loaddata", fixture_path)
            print("Initial doctor fixtures loaded successfully.")
except Exception as exc:
    print(f"Notice: Initial data fixture loading skipped or encountered: {exc}")
