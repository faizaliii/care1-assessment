import { Patient } from '../types';

interface PatientListProps {
  patients: Patient[];
  loading: boolean;
  onEdit: (patient: Patient) => void;
  onDelete: (patient: Patient) => void;
}

function PatientList({ patients, loading, onEdit, onDelete }: PatientListProps) {
  if (loading) {
    return <div className="loading">Loading patients...</div>;
  }

  if (patients.length === 0) {
    return (
      <div className="empty-state">
        <p>No patients found for this clinic.</p>
        <p>Click "Add Patient" to add your first patient.</p>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="patients-table">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Date of Birth</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((patient) => (
            <tr key={patient.id}>
              <td>{patient.full_name}</td>
              <td>{formatDate(patient.date_of_birth)}</td>
              <td>{patient.email || '-'}</td>
              <td>{patient.phone || '-'}</td>
              <td className="actions">
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => onEdit(patient)}
                >
                  Edit
                </button>
                <button
                  className="btn btn-danger btn-sm"
                  onClick={() => onDelete(patient)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PatientList;
