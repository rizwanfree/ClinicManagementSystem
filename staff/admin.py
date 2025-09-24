from django.contrib import admin

from staff.models import Staff

# Register your models here.


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "role", "phone", "email")
    list_filter = ("role",)
    search_fields = ("first_name", "last_name", "phone", "email")