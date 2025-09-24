# appointments/views.py
from django.shortcuts import render
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .models import Appointment



@login_required
def appointments_table(request):
    # Get date from query string (?date=YYYY-MM-DD), else today
    date_str = request.GET.get("date")
    if date_str:
        from datetime import datetime
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        selected_date = now().date()

    appointments = Appointment.objects.filter(date=selected_date)

    print("Selected date:", selected_date)
    print("Appointments:", appointments.query)
    
    context = {
    "appointments": appointments,
    "selected_date": selected_date,
    "prev_date": selected_date - timedelta(days=1),
    "next_date": selected_date + timedelta(days=1),
    }
    return render(request, "appointments/appointments_table.html", context)
