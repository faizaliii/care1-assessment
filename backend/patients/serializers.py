"""
Serializers for the Patient Management API.

These serializers handle the conversion between model instances
and JSON representations for the REST API.
"""
from rest_framework import serializers
from .models import Clinic, Patient, Clinician, Appointment


class ClinicSerializer(serializers.ModelSerializer):
    """Serializer for Clinic model."""
    
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address', 'phone', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ClinicianSerializer(serializers.ModelSerializer):
    """Serializer for Clinician model."""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Clinician
        fields = ['id', 'clinic', 'first_name', 'last_name', 'full_name', 
                  'specialty', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"Dr. {obj.first_name} {obj.last_name}"


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model."""
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['id', 'clinic', 'first_name', 'last_name', 'full_name',
                  'date_of_birth', 'email', 'phone', 'address', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model."""
    clinicians = ClinicianSerializer(many=True, read_only=True)
    clinician_ids = serializers.PrimaryKeyRelatedField(
        queryset=Clinician.objects.all(),
        many=True,
        write_only=True,
        source='clinicians'
    )
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'patient_name', 'clinicians', 'clinician_ids',
                  'appointment_date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
