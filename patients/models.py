from django.db import models

# Create your models here.


class Patient(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    mr_number = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)  # auto-generated
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(verbose_name="Date of Birth")
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)   # when record created
    updated_at = models.DateTimeField(auto_now=True)       # when record last updated

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.mr_number:
            last_patient = Patient.objects.exclude(mr_number__isnull=True).exclude(mr_number="").order_by("id").last()
            if last_patient and last_patient.mr_number:
                try:
                    last_number = int(last_patient.mr_number.split("-")[-1])
                except (ValueError, IndexError):
                    last_number = 0
                new_number = last_number + 1
            else:
                new_number = 1

            # Keep generating until we find a free one
            mr_candidate = f"MR-{new_number:05d}"
            while Patient.objects.filter(mr_number=mr_candidate).exists():
                new_number += 1
                mr_candidate = f"MR-{new_number:05d}"

            self.mr_number = mr_candidate

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.first_name} (MR No: {self.mr_number})"