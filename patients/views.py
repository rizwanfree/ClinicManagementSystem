from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from appointments.models import Appointment
from billing.models import Bill
from doctors.models import Doctor
from records.models import MedicalRecord, Prescription
from .models import Patient

@login_required
def patients_list(request):
    patients = Patient.objects.all()
    
    return render(request, "patients/patients_list.html", {"patients": patients})

@login_required
def patients_create(request):
    if request.method == "POST":
        patient = Patient.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            dob=request.POST.get("dob"),
            gender=request.POST.get("gender"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
        )
        messages.success(request, "Patient created successfully!")
    return redirect("patients_list")



def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    # Appointments
    today = timezone.now().date()
    upcoming_appointments = (
        Appointment.objects.filter(patient=patient, date__gte=today)
        .order_by("date", "time")
    )
    past_appointments = (
        Appointment.objects.filter(patient=patient, date__lt=today)
        .order_by("-date", "-time")
    )

    # Prescriptions via MedicalRecord
    prescriptions = Prescription.objects.filter(record__patient=patient)

    # Invoices (Bills)
    invoices = Bill.objects.filter(patient=patient)

    # Health Records
    health_records = MedicalRecord.objects.filter(patient=patient).order_by("-visit_date")

    context = {
        "patients": Patient.objects.all(),
        "doctors": Doctor.objects.all(),
        "patient": patient,
        "upcoming_appointments": upcoming_appointments,
        "past_appointments": past_appointments,
        "prescriptions": prescriptions,
        "invoices": invoices,
        "health_records": health_records,
        "selected_patient": patient,   # 👈 preselect this one

        # history grouped
        "diagnosis_history": patient.history_items.filter(category="CURRENT_DIAGNOSIS"),
        "past_medical_history": patient.history_items.filter(category="PAST_MEDICAL"),
        "family_history": patient.history_items.filter(category="FAMILY"),
        "surgical_history": patient.history_items.filter(category="SURGICAL"),
        "allergy_history": patient.history_items.filter(category="ALLERGIES"),
    }
    return render(request, "patients/patient_detail.html", context)