# patients/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from patients.models import Patient, PatientVital, HistoryItem
from appointments.models import Appointment
from records.models import MedicalRecord, Prescription
from billing.models import Bill
from doctors.models import Doctor

fake = Faker("en_PK")  # Pakistani locale

class Command(BaseCommand):
    help = "Seed database with sample patients and related data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # make sure at least 3 doctors exist
        doctors = list(Doctor.objects.all())
        if not doctors:
            for i in range(3):
                doctors.append(Doctor.objects.create(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    specialty=random.choice(["Cardiologist", "General Physician", "Dermatologist"]),
                    phone=fake.phone_number(),
                    email=fake.email(),
                ))

        for _ in range(100):  # create 100 patients
            patient = Patient.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                dob=fake.date_of_birth(minimum_age=10, maximum_age=80),
                gender=random.choice(["M", "F"]),
                phone=fake.phone_number(),
                email=fake.email(),
                address=fake.address(),
            )

            # Add some vitals
            for _ in range(random.randint(1, 3)):
                PatientVital.objects.create(
                    patient=patient,
                    height_cm=random.uniform(150, 190),
                    weight_kg=random.uniform(50, 100),
                    bp=f"{random.randint(100, 140)}/{random.randint(60, 90)}",
                    pulse=random.randint(60, 100),
                    temperature_c=round(random.uniform(36.5, 38.0), 1),
                    notes="Auto-generated",
                )

            # Add medical history
            for category, _ in HistoryItem.HISTORY_CHOICES:
                if random.random() > 0.5:
                    HistoryItem.objects.create(
                        patient=patient,
                        category=category,
                        description=fake.sentence(nb_words=8),
                    )

            # Create appointments (past + upcoming)
            for _ in range(random.randint(2, 5)):
                appointment_date = fake.date_between(start_date="-1y", end_date="+1m")
                Appointment.objects.create(
                    patient=patient,
                    doctor=random.choice(doctors),
                    date=appointment_date,
                    time=fake.time(pattern="%H:%M"),
                    status=random.choice(["Scheduled", "Completed", "Cancelled"]),
                    notes=fake.sentence(),
                )

            # Medical records + prescriptions
            for _ in range(random.randint(1, 3)):
                record = MedicalRecord.objects.create(
                    patient=patient,
                    doctor=random.choice(doctors),
                    diagnosis=fake.sentence(),
                    treatment=fake.sentence(),
                )
                for _ in range(random.randint(1, 2)):
                    Prescription.objects.create(
                        record=record,
                        medication_name=random.choice(["Paracetamol", "Ibuprofen", "Amoxicillin"]),
                        dosage=f"{random.randint(1, 2)} tablet(s)",
                        duration=f"{random.randint(3, 10)} days",
                    )

            # Bills
            for _ in range(random.randint(1, 2)):
                total = random.randint(500, 5000)
                paid = random.choice([0, total])  # either unpaid or fully paid for now
                Bill.objects.create(
                    patient=patient,
                    total_amount=total,      # ✅ correct field
                    paid_amount=paid,        # ✅ correct field
                    status="PAID" if paid else "PENDING",
                    payment_date=fake.date_this_year() if paid else None,
                )

        self.stdout.write(self.style.SUCCESS("✅ Seeding completed."))
