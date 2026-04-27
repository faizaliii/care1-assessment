import { Clinic, Patient, PatientFormData } from './types';

const API_BASE = '/api';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || `HTTP error! status: ${response.status}`);
  }
  if (response.status === 204) {
    return {} as T;
  }
  return response.json();
}

export async function fetchClinics(): Promise<Clinic[]> {
  const response = await fetch(`${API_BASE}/clinics/`);
  return handleResponse<Clinic[]>(response);
}

export async function fetchPatients(clinicId?: number): Promise<Patient[]> {
  const url = clinicId 
    ? `${API_BASE}/patients/?clinic_id=${clinicId}`
    : `${API_BASE}/patients/`;
  const response = await fetch(url);
  return handleResponse<Patient[]>(response);
}

export async function fetchPatient(id: number): Promise<Patient> {
  const response = await fetch(`${API_BASE}/patients/${id}/`);
  return handleResponse<Patient>(response);
}

export async function createPatient(clinicId: number, data: PatientFormData): Promise<Patient> {
  const response = await fetch(`${API_BASE}/patients/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ ...data, clinic: clinicId }),
  });
  return handleResponse<Patient>(response);
}

export async function updatePatient(id: number, clinicId: number, data: PatientFormData): Promise<Patient> {
  const response = await fetch(`${API_BASE}/patients/${id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ ...data, clinic: clinicId }),
  });
  return handleResponse<Patient>(response);
}

export async function deletePatient(id: number): Promise<void> {
  const response = await fetch(`${API_BASE}/patients/${id}/`, {
    method: 'DELETE',
  });
  await handleResponse<void>(response);
}
