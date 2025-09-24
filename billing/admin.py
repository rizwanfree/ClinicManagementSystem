from django.contrib import admin

from billing.models import Bill

# Register your models here.

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "appointment", "total_amount", "paid_amount", "status", "payment_date")
    list_filter = ("status", "payment_date")
    search_fields = ("patient__first_name", "patient__last_name")