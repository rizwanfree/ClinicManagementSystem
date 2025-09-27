from django.db import models, transaction
from django.utils import timezone
from datetime import date

# Create your models here.


GENDER_CHOICES = [("M", "Male"), ("F", "Female")]

class Patient(models.Model):
    mr_number = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} (MR: {self.mr_number})"

    @property
    def age(self):
        if not self.dob:
            return None
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    def _generate_mr(self):
        """Generate next MR candidate in a transaction-safe way."""
        # Use select_for_update to avoid race in high-concurrency scenarios
        with transaction.atomic():
            last = (
                Patient.objects
                .select_for_update()
                .exclude(mr_number__isnull=True)
                .exclude(mr_number="")
                .order_by("id")
                .last()
            )
            last_num = 0
            if last and last.mr_number:
                try:
                    last_num = int(last.mr_number.split("-")[-1])
                except Exception:
                    last_num = 0
            new_num = last_num + 1
            candidate = f"MR-{new_num:05d}"
            # ensure uniqueness
            while Patient.objects.filter(mr_number=candidate).exists():
                new_num += 1
                candidate = f"MR-{new_num:05d}"
            return candidate

    def save(self, *args, **kwargs):
        if not self.mr_number:
            self.mr_number = self._generate_mr()
        super().save(*args, **kwargs)


class PatientVital(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="vitals")
    recorded_at = models.DateTimeField(auto_now_add=True)
    height_cm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    bp = models.CharField(max_length=20, null=True, blank=True)  # "120/80"
    pulse = models.PositiveIntegerField(null=True, blank=True)
    temperature_c = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-recorded_at"]


class HistoryItem(models.Model):
    HISTORY_CHOICES = [
        ("CURRENT_DIAGNOSIS", "Current Diagnosis"),
        ("PAST_MEDICAL", "Past Medical History"),
        ("FAMILY", "Family History"),
        ("SURGICAL", "Surgical History"),
        ("ALLERGIES", "Allergies"),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="history_items")
    category = models.CharField(max_length=30, choices=HISTORY_CHOICES)
    description = models.TextField()
    noted_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-noted_at"]