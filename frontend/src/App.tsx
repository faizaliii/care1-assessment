import { useState, useEffect, useCallback } from 'react';
import { Clinic, Patient, PatientFormData } from './types';
import { fetchClinics, fetchPatients, createPatient, updatePatient, deletePatient } from './api';
import PatientList from './components/PatientList';
import PatientForm from './components/PatientForm';

function App() {
  const [clinics, setClinics] = useState<Clinic[]>([]);
  const [selectedClinicId, setSelectedClinicId] = useState<number | null>(null);
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingPatient, setEditingPatient] = useState<Patient | null>(null);

  const loadClinics = useCallback(async () => {
    try {
      const data = await fetchClinics();
      setClinics(data);
      if (data.length > 0 && !selectedClinicId) {
        setSelectedClinicId(data[0].id);
      }
    } catch (err) {
      setError('Failed to load clinics. Please try again.');
      console.error(err);
    }
  }, [selectedClinicId]);

  const loadPatients = useCallback(async () => {
    if (!selectedClinicId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await fetchPatients(selectedClinicId);
      setPatients(data);
    } catch (err) {
      setError('Failed to load patients. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [selectedClinicId]);

  useEffect(() => {
    loadClinics();
  }, [loadClinics]);

  useEffect(() => {
    if (selectedClinicId) {
      loadPatients();
    }
  }, [selectedClinicId, loadPatients]);

  const handleAddPatient = () => {
    setEditingPatient(null);
    setShowForm(true);
  };

  const handleEditPatient = (patient: Patient) => {
    setEditingPatient(patient);
    setShowForm(true);
  };

  const handleDeletePatient = async (patient: Patient) => {
    if (!window.confirm(`Are you sure you want to delete ${patient.full_name}?`)) {
      return;
    }
    try {
      await deletePatient(patient.id);
      await loadPatients();
    } catch (err) {
      setError('Failed to delete patient. Please try again.');
      console.error(err);
    }
  };

  const handleFormSubmit = async (data: PatientFormData) => {
    if (!selectedClinicId) return;
    try {
      if (editingPatient) {
        await updatePatient(editingPatient.id, selectedClinicId, data);
      } else {
        await createPatient(selectedClinicId, data);
      }
      setShowForm(false);
      setEditingPatient(null);
      await loadPatients();
    } catch (err) {
      setError('Failed to save patient. Please try again.');
      console.error(err);
    }
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingPatient(null);
  };

  return (
    <div className="container">
      <header>
        <h1>Patient Management</h1>
      </header>

      <div className="clinic-selector">
        <label htmlFor="clinic-select">Select Clinic:</label>
        <select
          id="clinic-select"
          value={selectedClinicId || ''}
          onChange={(e) => setSelectedClinicId(Number(e.target.value))}
        >
          {clinics.map((clinic) => (
            <option key={clinic.id} value={clinic.id}>
              {clinic.name}
            </option>
          ))}
        </select>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="actions-bar">
        <h2>Patients</h2>
        <button className="btn btn-primary" onClick={handleAddPatient}>
          Add Patient
        </button>
      </div>

      <PatientList
        patients={patients}
        loading={loading}
        onEdit={handleEditPatient}
        onDelete={handleDeletePatient}
      />

      {showForm && (
        <PatientForm
          patient={editingPatient}
          onSubmit={handleFormSubmit}
          onCancel={handleFormCancel}
        />
      )}
    </div>
  );
}

export default App;
