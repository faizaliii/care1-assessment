"""
Views for the Patient Management API.

Provides ViewSets for CRUD operations on Clinic, Patient, Clinician, 
and Appointment models.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Clinic, Patient, Clinician, Appointment
from .serializers import (
    ClinicSerializer, 
    PatientSerializer, 
    ClinicianSerializer, 
    AppointmentSerializer
)


class ClinicViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing clinics.
    
    Provides list, create, retrieve, update, and destroy actions.
    """
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patients.
    
    Supports filtering by clinic_id query parameter to get patients
    belonging to a specific clinic.
    """
    serializer_class = PatientSerializer
    
    def get_queryset(self):
        """
        Optionally filter patients by clinic_id query parameter.
        """
        queryset = Patient.objects.all()
        clinic_id = self.request.query_params.get('clinic_id')
        if clinic_id is not None:
            queryset = queryset.filter(clinic_id=clinic_id)
        return queryset


class ClinicianViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing clinicians.
    
    Supports filtering by clinic_id query parameter.
    """
    serializer_class = ClinicianSerializer
    
    def get_queryset(self):
        """
        Optionally filter clinicians by clinic_id query parameter.
        """
        queryset = Clinician.objects.all()
        clinic_id = self.request.query_params.get('clinic_id')
        if clinic_id is not None:
            queryset = queryset.filter(clinic_id=clinic_id)
        return queryset


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing appointments.
    
    Supports filtering by patient_id query parameter.
    """
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        """
        Optionally filter appointments by patient_id query parameter.
        """
        queryset = Appointment.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id is not None:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset
