"""
Admin configuration for the Patient Management application.

Registers models with customized admin interfaces for easier management.
"""
from django.contrib import admin
from .models import Clinic, Patient, Clinician, Appointment


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    """Admin interface for Clinic model."""
    list_display = ['name', 'phone', 'created_at']
    search_fields = ['name', 'address']
    ordering = ['name']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Admin interface for Patient model."""
    list_display = ['last_name', 'first_name', 'clinic', 'date_of_birth', 'phone']
    list_filter = ['clinic']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['last_name', 'first_name']


@admin.register(Clinician)
class ClinicianAdmin(admin.ModelAdmin):
    """Admin interface for Clinician model."""
    list_display = ['last_name', 'first_name', 'clinic', 'specialty']
    list_filter = ['clinic', 'specialty']
    search_fields = ['first_name', 'last_name', 'specialty']
    ordering = ['last_name', 'first_name']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Admin interface for Appointment model."""
    list_display = ['patient', 'appointment_date', 'get_clinicians']
    list_filter = ['appointment_date', 'patient__clinic']
    search_fields = ['patient__first_name', 'patient__last_name', 'notes']
    ordering = ['-appointment_date']
    
    def get_clinicians(self, obj):
        """Display comma-separated list of clinicians."""
        return ", ".join([str(c) for c in obj.clinicians.all()])
    get_clinicians.short_description = 'Clinicians'
