
from django.urls import path

from . import views

urlpatterns = [    
    path("", views.patients_list, name="patients_list"),
    path("create/", views.patients_create, name="patients_create"),
    path("<int:pk>/", views.patient_detail, name="patient_detail"),
]
