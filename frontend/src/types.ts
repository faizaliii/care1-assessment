export interface Clinic {
  id: number;
  name: string;
  address: string;
  phone: string;
  created_at: string;
  updated_at: string;
}

export interface Patient {
  id: number;
  clinic: number;
  first_name: string;
  last_name: string;
  full_name: string;
  date_of_birth: string;
  email: string;
  phone: string;
  address: string;
  created_at: string;
  updated_at: string;
}

export interface PatientFormData {
  first_name: string;
  last_name: string;
  date_of_birth: string;
  email: string;
  phone: string;
  address: string;
}
