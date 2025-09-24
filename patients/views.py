from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
            age=request.POST.get("age"),
            gender=request.POST.get("gender"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
        )
        messages.success(request, "Patient created successfully!")
    return redirect("patients_list")
