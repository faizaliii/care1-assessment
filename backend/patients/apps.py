"""
App configuration for the patients application.
"""
from django.apps import AppConfig


class PatientsConfig(AppConfig):
    """Configuration class for the patients app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patients'
    verbose_name = 'Patient Management'
