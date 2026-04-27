"""
Unit tests for the Patient Management API.

Tests cover CRUD operations for all models via the REST API endpoints.
"""
from datetime import date, datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Clinic, Patient, Clinician, Appointment


class ClinicModelTest(TestCase):
    """Tests for the Clinic model."""
    
    def test_clinic_str_representation(self):
        """Test string representation of Clinic."""
        clinic = Clinic.objects.create(name="Test Clinic")
        self.assertEqual(str(clinic), "Test Clinic")


class PatientModelTest(TestCase):
    """Tests for the Patient model."""
    
    def setUp(self):
        self.clinic = Clinic.objects.create(name="Test Clinic")
    
    def test_patient_str_representation_with_name(self):
        """Test string representation of Patient with full name."""
        patient = Patient.objects.create(
            clinic=self.clinic,
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            email="john.doe@example.com"
        )
        self.assertEqual(str(patient), "John Doe")
    
    def test_patient_str_representation_without_first_name(self):
        """Test string representation of Patient without first name."""
        patient = Patient.objects.create(
            clinic=self.clinic,
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            email="doe@example.com"
        )
        self.assertEqual(str(patient), "Doe")
    
    def test_patient_full_name_property(self):
        """Test full_name property of Patient."""
        patient = Patient.objects.create(
            clinic=self.clinic,
            first_name="Jane",
            last_name="Smith",
            date_of_birth=date(1985, 5, 15),
            email="jane.smith@example.com"
        )
        self.assertEqual(patient.full_name, "Jane Smith")
    
    def test_patient_full_name_without_first_name(self):
        """Test full_name property when first_name is empty."""
        patient = Patient.objects.create(
            clinic=self.clinic,
            last_name="Smith",
            date_of_birth=date(1985, 5, 15),
            email="smith@example.com"
        )
        self.assertEqual(patient.full_name, "Smith")


class ClinicianModelTest(TestCase):
    """Tests for the Clinician model."""
    
    def setUp(self):
        self.clinic = Clinic.objects.create(name="Test Clinic")
    
    def test_clinician_str_representation(self):
        """Test string representation of Clinician."""
        clinician = Clinician.objects.create(
            clinic=self.clinic,
            first_name="Alice",
            last_name="Johnson",
            specialty="Cardiology"
        )
        self.assertEqual(str(clinician), "Dr. Alice Johnson")


class PatientAPITest(APITestCase):
    """Tests for the Patient API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.clinic = Clinic.objects.create(
            name="Main Clinic",
            address="123 Medical St",
            phone="555-0100"
        )
        self.clinic2 = Clinic.objects.create(
            name="Secondary Clinic",
            address="456 Health Ave",
            phone="555-0200"
        )
        self.patient = Patient.objects.create(
            clinic=self.clinic,
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 15),
            email="john.doe@example.com",
            phone="555-1234"
        )
    
    def test_list_patients(self):
        """Test listing all patients."""
        url = reverse('patient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_list_patients_filtered_by_clinic(self):
        """Test filtering patients by clinic_id."""
        Patient.objects.create(
            clinic=self.clinic2,
            first_name="Jane",
            last_name="Smith",
            date_of_birth=date(1985, 5, 20),
            email="jane.smith@example.com"
        )
        url = reverse('patient-list')
        response = self.client.get(url, {'clinic_id': self.clinic.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'John')
    
    def test_create_patient(self):
        """Test creating a new patient."""
        url = reverse('patient-list')
        data = {
            'clinic': self.clinic.id,
            'first_name': 'Alice',
            'last_name': 'Brown',
            'date_of_birth': '1995-03-10',
            'email': 'alice.brown@example.com',
            'phone': '555-5678'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 2)
        self.assertEqual(response.data['first_name'], 'Alice')
    
    def test_create_patient_without_first_name(self):
        """Test creating a patient without first name (optional field)."""
        url = reverse('patient-list')
        data = {
            'clinic': self.clinic.id,
            'last_name': 'Wilson',
            'date_of_birth': '1995-03-10',
            'email': 'wilson@example.com',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], '')
    
    def test_create_patient_missing_email(self):
        """Test creating patient without email fails (required field)."""
        url = reverse('patient-list')
        data = {
            'clinic': self.clinic.id,
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '1995-03-10',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_retrieve_patient(self):
        """Test retrieving a specific patient."""
        url = reverse('patient-detail', kwargs={'pk': self.patient.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['full_name'], 'John Doe')
    
    def test_update_patient(self):
        """Test updating a patient."""
        url = reverse('patient-detail', kwargs={'pk': self.patient.id})
        data = {
            'clinic': self.clinic.id,
            'first_name': 'Johnny',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-15',
            'email': 'johnny.doe@example.com',
            'phone': '555-9999'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.first_name, 'Johnny')
        self.assertEqual(self.patient.phone, '555-9999')
    
    def test_partial_update_patient(self):
        """Test partial update of a patient."""
        url = reverse('patient-detail', kwargs={'pk': self.patient.id})
        data = {'phone': '555-0000'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.phone, '555-0000')
    
    def test_delete_patient(self):
        """Test deleting a patient."""
        url = reverse('patient-detail', kwargs={'pk': self.patient.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Patient.objects.count(), 0)
    
    def test_create_patient_missing_required_fields(self):
        """Test creating patient with missing required fields."""
        url = reverse('patient-list')
        data = {
            'clinic': self.clinic.id,
            'first_name': 'Test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ClinicAPITest(APITestCase):
    """Tests for the Clinic API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.clinic = Clinic.objects.create(
            name="Test Clinic",
            address="123 Test St",
            phone="555-0001"
        )
    
    def test_list_clinics(self):
        """Test listing all clinics."""
        url = reverse('clinic-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_clinic(self):
        """Test creating a new clinic."""
        url = reverse('clinic-list')
        data = {
            'name': 'New Clinic',
            'address': '456 New Ave',
            'phone': '555-0002'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Clinic.objects.count(), 2)
    
    def test_retrieve_clinic(self):
        """Test retrieving a specific clinic."""
        url = reverse('clinic-detail', kwargs={'pk': self.clinic.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Clinic')


class ClinicianAPITest(APITestCase):
    """Tests for the Clinician API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.clinic = Clinic.objects.create(name="Test Clinic")
        self.clinician = Clinician.objects.create(
            clinic=self.clinic,
            first_name="Alice",
            last_name="Smith",
            specialty="Cardiology",
            email="alice.smith@clinic.com"
        )
    
    def test_list_clinicians(self):
        """Test listing all clinicians."""
        url = reverse('clinician-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_list_clinicians_filtered_by_clinic(self):
        """Test filtering clinicians by clinic_id."""
        clinic2 = Clinic.objects.create(name="Other Clinic")
        Clinician.objects.create(
            clinic=clinic2,
            first_name="Bob",
            last_name="Jones",
            specialty="Neurology"
        )
        url = reverse('clinician-list')
        response = self.client.get(url, {'clinic_id': self.clinic.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Alice')
    
    def test_create_clinician(self):
        """Test creating a new clinician."""
        url = reverse('clinician-list')
        data = {
            'clinic': self.clinic.id,
            'first_name': 'Bob',
            'last_name': 'Wilson',
            'specialty': 'Dermatology',
            'email': 'bob.wilson@clinic.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Clinician.objects.count(), 2)


class AppointmentAPITest(APITestCase):
    """Tests for the Appointment API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.clinic = Clinic.objects.create(name="Test Clinic")
        self.patient = Patient.objects.create(
            clinic=self.clinic,
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            email="john.doe@example.com"
        )
        self.clinician = Clinician.objects.create(
            clinic=self.clinic,
            first_name="Dr",
            last_name="Smith",
            specialty="General"
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            appointment_date=datetime(2024, 6, 15, 10, 0),
            notes="Regular checkup"
        )
        self.appointment.clinicians.add(self.clinician)
    
    def test_list_appointments(self):
        """Test listing all appointments."""
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_list_appointments_filtered_by_patient(self):
        """Test filtering appointments by patient_id."""
        patient2 = Patient.objects.create(
            clinic=self.clinic,
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1985, 5, 15),
            email="jane.doe@example.com"
        )
        Appointment.objects.create(
            patient=patient2,
            appointment_date=datetime(2024, 6, 20, 14, 0)
        )
        url = reverse('appointment-list')
        response = self.client.get(url, {'patient_id': self.patient.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_appointment(self):
        """Test creating a new appointment with clinicians."""
        url = reverse('appointment-list')
        data = {
            'patient': self.patient.id,
            'appointment_date': '2024-07-01T09:00:00Z',
            'notes': 'Follow-up visit',
            'clinician_ids': [self.clinician.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)
