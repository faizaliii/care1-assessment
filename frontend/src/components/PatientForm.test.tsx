import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import PatientForm from './PatientForm';
import { Patient } from '../types';

const mockPatient: Patient = {
  id: 1,
  clinic: 1,
  first_name: 'John',
  last_name: 'Doe',
  full_name: 'John Doe',
  date_of_birth: '1990-01-15',
  email: 'john.doe@example.com',
  phone: '555-1234',
  address: '123 Main St',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

describe('PatientForm', () => {
  it('renders add patient form when no patient is provided', () => {
    render(
      <PatientForm
        patient={null}
        onSubmit={() => {}}
        onCancel={() => {}}
      />
    );
    
    expect(screen.getByText('Add Patient')).toBeInTheDocument();
    expect(screen.getByLabelText('First Name *')).toHaveValue('');
    expect(screen.getByLabelText('Last Name *')).toHaveValue('');
  });

  it('renders edit patient form with patient data', () => {
    render(
      <PatientForm
        patient={mockPatient}
        onSubmit={() => {}}
        onCancel={() => {}}
      />
    );
    
    expect(screen.getByText('Edit Patient')).toBeInTheDocument();
    expect(screen.getByLabelText('First Name *')).toHaveValue('John');
    expect(screen.getByLabelText('Last Name *')).toHaveValue('Doe');
    expect(screen.getByLabelText('Date of Birth *')).toHaveValue('1990-01-15');
    expect(screen.getByLabelText('Email')).toHaveValue('john.doe@example.com');
  });

  it('shows validation errors for required fields', () => {
    const onSubmit = vi.fn();
    render(
      <PatientForm
        patient={null}
        onSubmit={onSubmit}
        onCancel={() => {}}
      />
    );
    
    fireEvent.click(screen.getByText('Add Patient'));
    
    expect(screen.getByText('First name is required')).toBeInTheDocument();
    expect(screen.getByText('Last name is required')).toBeInTheDocument();
    expect(screen.getByText('Date of birth is required')).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('calls onSubmit with form data when valid', () => {
    const onSubmit = vi.fn();
    render(
      <PatientForm
        patient={null}
        onSubmit={onSubmit}
        onCancel={() => {}}
      />
    );
    
    fireEvent.change(screen.getByLabelText('First Name *'), { target: { value: 'Jane' } });
    fireEvent.change(screen.getByLabelText('Last Name *'), { target: { value: 'Smith' } });
    fireEvent.change(screen.getByLabelText('Date of Birth *'), { target: { value: '1985-05-20' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'jane@example.com' } });
    
    fireEvent.click(screen.getByText('Add Patient'));
    
    expect(onSubmit).toHaveBeenCalledWith({
      first_name: 'Jane',
      last_name: 'Smith',
      date_of_birth: '1985-05-20',
      email: 'jane@example.com',
      phone: '',
      address: '',
    });
  });

  it('calls onCancel when cancel button is clicked', () => {
    const onCancel = vi.fn();
    render(
      <PatientForm
        patient={null}
        onSubmit={() => {}}
        onCancel={onCancel}
      />
    );
    
    fireEvent.click(screen.getByText('Cancel'));
    
    expect(onCancel).toHaveBeenCalled();
  });

  it('calls onCancel when clicking overlay', () => {
    const onCancel = vi.fn();
    render(
      <PatientForm
        patient={null}
        onSubmit={() => {}}
        onCancel={onCancel}
      />
    );
    
    fireEvent.click(document.querySelector('.modal-overlay')!);
    
    expect(onCancel).toHaveBeenCalled();
  });
});
