from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime
from django.db.models import Count, Sum



from billing.models import Bill
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

def create_appointment(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")
        date = request.POST.get("date")
        time = request.POST.get("time") or None  # 👈 Fix: empty string becomes None
        status = request.POST.get("status", "SCHEDULED")
        notes = request.POST.get("notes", "")

        # Create Appointment
        appointment = Appointment.objects.create(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date,
            time=time,
            status=status,
            notes=notes,
        )

        # --- Auto create Bill ---
        doctor = appointment.doctor
        total_amount = getattr(doctor, "fee", 0)  # default to doctor fee, or 0 if not set
        paid_now = request.POST.get("paid_now")  # checkbox or hidden input

        Bill.objects.create(
            appointment=appointment,
            patient=appointment.patient,
            total_amount=total_amount,
            paid_amount=total_amount if paid_now else 0,
            status="PAID" if paid_now else "PENDING",
            payment_date=now().date() if paid_now else None,
        )

        return redirect("dashboard")  # adjust target

@login_required
def dashboard(request):
    role = request.user.role

    # Handle selected date (for doctors/staff)
    date_str = request.GET.get("date")
    if date_str:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        selected_date = now().date()

    context = {
        "selected_date": selected_date,
        "prev_date": selected_date - timedelta(days=1),
        "next_date": selected_date + timedelta(days=1),
    }

    # ---------------- Staff Dashboard ----------------
    if role == "STAFF":
        appointments = Appointment.objects.filter(date=selected_date)

        context.update({
            "patients": Patient.objects.all(),
            "doctors": Doctor.objects.all(),
            "patients_count": Patient.objects.count(),
            "appointments_count_today": Appointment.objects.filter(date=now().date()).count(),
            "appointments_count_total": Appointment.objects.count(),
            "appointments": appointments,
        })
        return render(request, "accounts/dashboard.html", context)

    # ---------------- Doctor Dashboard ----------------
    elif role == "DOCTOR":
        # doctor object must be linked to user
        doctor = getattr(request.user, "doctor", None)
        appointments = Appointment.objects.filter(date=selected_date, doctor=doctor)

        context.update({
            "appointments_today": appointments,
            "appointments_upcoming": Appointment.objects.filter(doctor=doctor, date__gte=now().date()).order_by("date", "time"),
            "patients_count": Patient.objects.filter(appointments__doctor=doctor).distinct().count(),
        })
        return render(request, "accounts/dashboard_doctor.html", context)

    # ---------------- Admin Dashboard ----------------
    elif role == "ADMIN":
        users_by_role = User.objects.values("role").annotate(count=Count("id"))
        revenue_total = Bill.objects.aggregate(total=Sum("amount"))["total"] or 0
        top_doctors = (
            Doctor.objects.annotate(app_count=Count("appointments"))
            .order_by("-app_count")[:5]
        )

        context.update({
            "patients_count": Patient.objects.count(),
            "doctors_count": Doctor.objects.count(),
            "users_by_role": users_by_role,
            "appointments_count_total": Appointment.objects.count(),
            "revenue_total": revenue_total,
            "top_doctors": top_doctors,
        })
        return render(request, "accounts/dashboard_admin.html", context)

    # Default fallback (STAFF layout)
    appointments = Appointment.objects.filter(date=selected_date)
    context.update({"appointments": appointments})
    return render(request, "accounts/dashboard_staff.html", context)