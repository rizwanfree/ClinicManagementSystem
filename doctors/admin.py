from django.contrib import admin

from doctors.models import Doctor

# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "specialty", "phone", "email")
    search_fields = ("first_name", "last_name", "specialty", "phone", "email")
    list_filter = ("specialty",)