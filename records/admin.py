from django.contrib import admin

from .models import MedicalRecord, Prescription



class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "visit_date", "diagnosis")
    list_filter = ("visit_date", "doctor")
    search_fields = ("patient__first_name", "patient__last_name", "doctor__first_name", "doctor__last_name", "diagnosis")
    inlines = [PrescriptionInline]

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("record", "medication_name", "dosage", "duration")
    search_fields = ("medication_name", "record__patient__first_name", "record__patient__last_name")
