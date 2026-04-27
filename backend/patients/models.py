"""
Models for the Patient Management application.

Database Schema:
- Clinic: Represents a medical clinic
- Patient: Belongs to one clinic, can have multiple appointments
- Clinician: Medical staff belonging to a clinic
- Appointment: Links a patient with one or more clinicians
"""
from django.db import models


class Clinic(models.Model):
    """
    Represents a medical clinic.
    Each clinic can have multiple patients and clinicians.
    """
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Patient(models.Model):
    """
    Represents a patient belonging to a specific clinic.
    """
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name='patients'
    )
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.email

    @property
    def full_name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.email


class Clinician(models.Model):
    """
    Represents a medical staff member (doctor, nurse, etc.) at a clinic.
    """
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name='clinicians'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"


class Appointment(models.Model):
    """
    Represents a patient appointment with one or more clinicians.
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    clinicians = models.ManyToManyField(
        Clinician,
        related_name='appointments'
    )
    appointment_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date']

    def __str__(self):
        return f"Appointment for {self.patient} on {self.appointment_date}"
