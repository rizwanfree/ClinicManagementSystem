from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime



from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

# Create your views here.


User = get_user_model()


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        role = request.POST.get("role")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Password do not match")
            return redirect("register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("register")
        
        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        login(request, user)
        return redirect("dashboard")
    
    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(user)
            login(request, user)
            return redirect("dashboard")
        else:
            print("user not found")
            messages.error(request, "Invalid username or password")
            return redirect("login")
        
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def create_appointment(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")
        date_val = request.POST.get("date")
        time_val = request.POST.get("time")
        status = request.POST.get("status")
        notes = request.POST.get("notes", "")

        if not patient_id or not doctor_id or not date_val:
            messages.error(request, "Patient, doctor, and date are required!")
            return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

        # handle optional time
        time_obj = now().time()
        if time_val:
            try:
                time_obj = datetime.strptime(time_val, "%H:%M").time()
            except ValueError:
                messages.error(request, "Time format is invalid. Use HH:MM.")
                return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

        Appointment.objects.create(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date_val,
            time=time_obj,  # can be None
            status=status,
            notes=notes,
        )

        messages.success(request, "Appointment created successfully!")

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_required
def dashboard(request):
    date_str = request.GET.get("date")
    if date_str:
        from datetime import datetime
        
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        selected_date = now().date()

    appointments = Appointment.objects.filter(date=selected_date)

    context = {
        "patients": Patient.objects.all(),
        "doctors": Doctor.objects.all(),
        "patients_count": Patient.objects.count(),
        "appointments_count_today": Appointment.objects.filter(date=now().date()).count(),
        "appointments_count_total": Appointment.objects.count(),
        "appointments": appointments,
        "selected_date": selected_date,
        "prev_date": selected_date - timedelta(days=1),
        "next_date": selected_date + timedelta(days=1),
    }
    return render(request, "accounts/dashboard.html", context)