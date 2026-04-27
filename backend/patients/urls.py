"""
URL configuration for the patients API.

Uses Django REST Framework's DefaultRouter to automatically generate
URL patterns for the ViewSets.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClinicViewSet, PatientViewSet, ClinicianViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'clinics', ClinicViewSet, basename='clinic')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'clinicians', ClinicianViewSet, basename='clinician')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
]
