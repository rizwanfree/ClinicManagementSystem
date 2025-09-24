from django.contrib import admin

from appointments.models import Appointment

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "date", "time", "status")
    list_filter = ("status", "date", "doctor")
    search_fields = ("patient__first_name", "patient__last_name", "doctor__first_name", "doctor__last_name")