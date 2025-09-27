from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from appointments.models import Appointment
from .models import Bill
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def create_invoice(request):
    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        appointment = get_object_or_404(Appointment, id=appointment_id)
        
        total_amount = request.POST.get("total_amount")
        paid_amount = request.POST.get("paid_amount")
        status = request.POST.get("status")

        Bill.objects.create(
            appointment=appointment,
            patient=appointment.patient,
            total_amount=total_amount,
            paid_amount=paid_amount,
            status=status,
            payment_date=now().date() if status == "PAID" else None,
        )
        messages.success(request, "Invoice created successfully!")
    return redirect("dashboard")