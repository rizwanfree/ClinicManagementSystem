from django.contrib import admin

from patients.models import Patient

# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "dob", "gender", "phone")
    search_fields = ("first_name", "last_name", "phone", "email")