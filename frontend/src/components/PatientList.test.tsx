import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import PatientList from './PatientList';
import { Patient } from '../types';

const mockPatients: Patient[] = [
  {
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
  },
  {
    id: 2,
    clinic: 1,
    first_name: 'Jane',
    last_name: 'Smith',
    full_name: 'Jane Smith',
    date_of_birth: '1985-05-20',
    email: '',
    phone: '',
    address: '',
    created_at: '2024-01-02T00:00:00Z',
    updated_at: '2024-01-02T00:00:00Z',
  },
];

describe('PatientList', () => {
  it('renders loading state', () => {
    render(
      <PatientList
        patients={[]}
        loading={true}
        onEdit={() => {}}
        onDelete={() => {}}
      />
    );
    expect(screen.getByText('Loading patients...')).toBeInTheDocument();
  });

  it('renders empty state when no patients', () => {
    render(
      <PatientList
        patients={[]}
        loading={false}
        onEdit={() => {}}
        onDelete={() => {}}
      />
    );
    expect(screen.getByText('No patients found for this clinic.')).toBeInTheDocument();
  });

  it('renders patient list correctly', () => {
    render(
      <PatientList
        patients={mockPatients}
        loading={false}
        onEdit={() => {}}
        onDelete={() => {}}
      />
    );
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    expect(screen.getByText('john.doe@example.com')).toBeInTheDocument();
    expect(screen.getByText('555-1234')).toBeInTheDocument();
  });

  it('displays dash for empty email and phone', () => {
    render(
      <PatientList
        patients={mockPatients}
        loading={false}
        onEdit={() => {}}
        onDelete={() => {}}
      />
    );
    
    const dashes = screen.getAllByText('-');
    expect(dashes.length).toBeGreaterThanOrEqual(2);
  });

  it('calls onEdit when edit button is clicked', () => {
    const onEdit = vi.fn();
    render(
      <PatientList
        patients={mockPatients}
        loading={false}
        onEdit={onEdit}
        onDelete={() => {}}
      />
    );
    
    const editButtons = screen.getAllByText('Edit');
    fireEvent.click(editButtons[0]);
    
    expect(onEdit).toHaveBeenCalledWith(mockPatients[0]);
  });

  it('calls onDelete when delete button is clicked', () => {
    const onDelete = vi.fn();
    render(
      <PatientList
        patients={mockPatients}
        loading={false}
        onEdit={() => {}}
        onDelete={onDelete}
      />
    );
    
    const deleteButtons = screen.getAllByText('Delete');
    fireEvent.click(deleteButtons[0]);
    
    expect(onDelete).toHaveBeenCalledWith(mockPatients[0]);
  });
});
