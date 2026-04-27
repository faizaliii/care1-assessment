# Patient Management System

A full-stack web application for clinics to manage their patients. Built with Django REST Framework and React + TypeScript.

## Features

- **Patient Management**: View, add, update, and delete patients
- **Multi-Clinic Support**: Each clinic has its own set of patients
- **Form Validation**: Email required (unique), last name required, date of birth required
- **RESTful API**: Full CRUD operations for patients, clinics, clinicians, and appointments

## Prerequisites

Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

To verify installation:
```bash
docker --version
docker compose version
```

## Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd care1-assessment
   ```

2. **Start the application**
   ```bash
   docker compose up --build
   ```

3. **Access the application**
   - **Frontend**: http://localhost
   - **API**: http://localhost/api
   - **Django Admin**: http://localhost/admin

The application comes pre-loaded with sample data (2 clinics, 3 patients).

## Stopping the Application

```bash
docker compose down
```

To remove the database volume as well:
```bash
docker compose down -v
```

## Running Tests

Tests run automatically via GitHub Actions on every pull request.

To run tests manually inside Docker:

```bash
# Backend tests
docker compose exec backend python manage.py test

# Frontend tests (requires rebuilding with test dependencies)
docker compose run --rm frontend npm test
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/patients/` | List all patients |
| GET | `/api/patients/?clinic_id={id}` | List patients by clinic |
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/{id}/` | Get patient details |
| PUT | `/api/patients/{id}/` | Update a patient |
| DELETE | `/api/patients/{id}/` | Delete a patient |
| GET | `/api/clinics/` | List all clinics |
| GET | `/api/clinicians/` | List all clinicians |
| GET | `/api/appointments/` | List all appointments |

## Project Structure

```
care1-assessment/
├── backend/                # Django REST API
│   ├── config/             # Settings and URLs
│   ├── patients/           # Models, views, serializers, tests
│   └── Dockerfile
├── frontend/               # React + TypeScript
│   ├── src/
│   │   ├── components/     # PatientList, PatientForm
│   │   ├── api.ts          # API client
│   │   └── types.ts        # TypeScript types
│   └── Dockerfile
├── .github/workflows/      # CI pipeline
├── docker-compose.yml
└── README.md
```

## Tech Stack

- **Backend**: Python 3.11, Django 4.2, Django REST Framework, PostgreSQL 15
- **Frontend**: React 18, TypeScript, Vite
- **DevOps**: Docker, Nginx, GitHub Actions

## Troubleshooting

**Port 80 already in use**
```bash
lsof -i :80
# Kill the process or change the port in docker-compose.yml
```

**Containers not starting**
```bash
docker compose logs
```

**Reset everything**
```bash
docker compose down -v
docker compose up --build
```
