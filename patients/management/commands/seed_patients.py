from django.core.management.base import BaseCommand
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from datetime import date, timedelta, time
import random

class Command(BaseCommand):
    help = "Seed dummy patients and appointments"

    def handle(self, *args, **options):
        # ----- Seed Patients -----
        male_names = [("Ahmed", "Khan"), ("Bilal", "Sheikh"), ("Hassan", "Ali"), ("Usman", "Raza"),
                      ("Zeeshan", "Farooq"), ("Tariq", "Mehmood"), ("Salman", "Qureshi"), ("Hamza", "Javed")]
        female_names = [("Ayesha", "Malik"), ("Fatima", "Hussain"), ("Zainab", "Chaudhry"),
                        ("Maryam", "Akhtar"), ("Sana", "Shah"), ("Hira", "Nawaz"), ("Khadija", "Iqbal")]

        def random_phone():
            return "03" + str(random.randint(10, 49)) + str(random.randint(1000000, 9999999))

        def random_age_dob():
            age = random.randint(18, 70)
            dob = date.today().replace(year=date.today().year - age)
            return age, dob

        patients = []
        for i in range(15):
            if i % 2 == 0:
                first, last = random.choice(male_names)
                gender = "M"
            else:
                first, last = random.choice(female_names)
                gender = "F"

            age, dob = random_age_dob()

            patient = Patient.objects.create(
                first_name=first,
                last_name=last,
                dob=dob,
                age=age,
                gender=gender,
                phone=random_phone(),
                email=f"{first.lower()}.{last.lower()}@example.com",
                address=f"{random.randint(10, 100)} Street, Lahore, Pakistan",
            )
            patients.append(patient)

        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(patients)} patients"))

        # ----- Seed Appointments -----

        doctors = list(Doctor.objects.all())
        if not doctors:
            self.stdout.write(self.style.WARNING("No doctors found. Seed doctors first!"))
            return

        appointments = []
        for patient in patients:
            # Random number of appointments per patient
            for _ in range(random.randint(1, 3)):
                doc = random.choice(doctors)
                appt_date = date.today() + timedelta(days=random.randint(0, 2))  # ✅ only today and future
                appt_time = time(hour=random.randint(9, 16), minute=random.choice([0, 15, 30, 45]))

                appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=doc,
                    date=appt_date,
                    time=appt_time,
                    status=random.choice(["SCHEDULED", "COMPLETED"]),  # optional: avoid CANCELLED initially
                )
                appointments.append(appointment)

        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(appointments)} appointments"))

