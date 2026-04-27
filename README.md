# Patient Management System

A full-stack web application for clinics to manage their patients. Built with Django REST Framework and React + TypeScript.

## Features

- **Patient Management**: View, add, update, and delete patients
- **Multi-Clinic Support**: Each clinic has its own set of patients
- **Modern UI**: Clean and responsive interface built with React
- **RESTful API**: Django REST Framework backend with full CRUD operations

## Tech Stack

### Backend
- **Python 3.11** - Programming language
- **Django 4.2** - Web framework
- **Django REST Framework** - API toolkit
- **PostgreSQL 15** - Database
- **Gunicorn** - WSGI HTTP Server

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Vitest** - Testing framework

### DevOps
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy and static file serving
- **GitHub Actions** - CI/CD pipeline

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

## Quick Start

### Running with Docker (Recommended)

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
   - Frontend: http://localhost
   - Django Admin: http://localhost/admin
   - API: http://localhost/api

The application comes pre-loaded with sample data (2 clinics, 3 clinicians, 3 patients).

### Stopping the Application

```bash
docker compose down
```

To also remove the database volume:
```bash
docker compose down -v
```

## Development Setup

### Backend Development

1. **Create a virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (or use defaults for development)
   ```bash
   export POSTGRES_DB=patient_management
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=postgres
   export POSTGRES_HOST=localhost
   export POSTGRES_PORT=5432
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load sample data (optional)**
   ```bash
   python manage.py loaddata initial_data.json
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

### Frontend Development

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```

The frontend dev server runs at http://localhost:3000 and proxies API requests to http://localhost:8000.

## Running Tests

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Running All Tests with Docker
Tests run automatically in the GitHub Actions CI pipeline on every push and pull request.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/clinics/` | List all clinics |
| POST | `/api/clinics/` | Create a clinic |
| GET | `/api/clinics/{id}/` | Get clinic details |
| PUT | `/api/clinics/{id}/` | Update a clinic |
| DELETE | `/api/clinics/{id}/` | Delete a clinic |
| GET | `/api/patients/` | List all patients |
| GET | `/api/patients/?clinic_id={id}` | List patients by clinic |
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/{id}/` | Get patient details |
| PUT | `/api/patients/{id}/` | Update a patient |
| DELETE | `/api/patients/{id}/` | Delete a patient |
| GET | `/api/clinicians/` | List all clinicians |
| GET | `/api/appointments/` | List all appointments |

## Project Structure

```
care1-assessment/
├── backend/
│   ├── config/             # Django settings and URL configuration
│   ├── patients/           # Main application with models, views, serializers
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.tsx         # Main application component
│   │   ├── api.ts          # API client functions
│   │   └── types.ts        # TypeScript type definitions
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI configuration
├── docker-compose.yml
└── README.md
```

## Database Schema

```
Clinic
├── id (PK)
├── name
├── address
├── phone
└── timestamps

Patient
├── id (PK)
├── clinic_id (FK → Clinic)
├── first_name
├── last_name
├── date_of_birth
├── email
├── phone
├── address
└── timestamps

Clinician
├── id (PK)
├── clinic_id (FK → Clinic)
├── first_name
├── last_name
├── specialty
├── email
└── timestamps

Appointment
├── id (PK)
├── patient_id (FK → Patient)
├── clinicians (M2M → Clinician)
├── appointment_date
├── notes
└── timestamps
```

## CI/CD

GitHub Actions runs automatically on:
- Push to `main` or `feature-branch`
- Pull request to `main`
- Manual trigger (workflow_dispatch)

The pipeline:
1. Runs backend tests with PostgreSQL
2. Runs frontend linting and tests
3. Builds Docker images to verify builds work

## Environment Variables

### Backend
| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | dev-secret-key |
| `DJANGO_DEBUG` | Enable debug mode | True |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts | localhost,127.0.0.1 |
| `POSTGRES_DB` | Database name | patient_management |
| `POSTGRES_USER` | Database user | postgres |
| `POSTGRES_PASSWORD` | Database password | postgres |
| `POSTGRES_HOST` | Database host | db |
| `POSTGRES_PORT` | Database port | 5432 |
| `CORS_ALLOWED_ORIGINS` | CORS origins | http://localhost:3000 |

## Troubleshooting

### Docker Issues

**Port already in use**
```bash
# Check what's using port 80
lsof -i :80
# Or use a different port in docker-compose.yml
```

**Database connection issues**
```bash
# Check if postgres is running
docker compose ps
# View postgres logs
docker compose logs db
```

**Rebuild containers after code changes**
```bash
docker compose up --build
```

### Development Issues

**Backend migrations not applying**
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

**Frontend build errors**
```bash
cd frontend
rm -rf node_modules
npm install
```

## License

This project is for assessment purposes.
