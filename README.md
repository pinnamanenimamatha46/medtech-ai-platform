# MedTech AI Platform

An enterprise-style healthcare technology platform built with **FastAPI, Python, SQLAlchemy, Pydantic, and AI-ready architecture**.

The project is designed as a portfolio-quality MedTech application that can evolve from core patient-management APIs into AI-assisted healthcare workflows, clinical data services, and intelligent healthcare automation.

## Project Status

Current milestone: **Patient Management API**

* FastAPI application structure
* Health-check API
* Patient database model
* Patient Pydantic schemas
* Patient service layer
* Create patient endpoint
* List patients endpoint
* Get patient by ID endpoint
* SQLAlchemy database integration
* Pydantic ORM response validation
* Ruff formatting and linting
* mypy static type checking
* pytest API testing

Current automated test status:

```text
4 passed
```

## Technology Stack

### Backend

* Python 3.11
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

### Database

* SQLite for local development
* Architecture prepared for future PostgreSQL integration

### Development & Quality

* uv
* Ruff
* mypy
* pytest
* pytest-asyncio
* HTTPX / FastAPI TestClient
* Git
* GitHub

## Project Structure

```text
medtech-ai-platform/
│
├── app/
│   ├── api/
│   │   └── patients.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   └── patient.py
│   │
│   ├── schemas/
│   │   └── patient.py
│   │
│   ├── services/
│   │   └── patient_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_health.py
│   └── test_patients.py
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
├── setup.md
└── uv.lock
```

## Architecture

The application follows a layered backend architecture:

```text
Client
  │
  ▼
FastAPI API Layer
  │
  ▼
Pydantic Schemas
  │
  ▼
Service Layer
  │
  ▼
SQLAlchemy Models
  │
  ▼
Database
```

This separation helps keep API routing, validation, business logic, and persistence concerns maintainable as the platform grows.

## Patient API

Base URL:

```text
/api/v1
```

### Create Patient

```http
POST /api/v1/patients
```

Example request:

```json
{
  "first_name": "Anita",
  "last_name": "Kotha",
  "date_of_birth": "1970-10-15",
  "email": "anita@example.com",
  "phone": "310-555-0101"
}
```

### List Patients

```http
GET /api/v1/patients
```

### Get Patient by ID

```http
GET /api/v1/patients/{patient_id}
```

### Health Check

```http
GET /api/v1/health
```

## Local Development

Clone the repository:

```bash
git clone <repository-url>
cd medtech-ai-platform
```

Install dependencies with `uv`:

```bash
uv sync
```

Run the application:

```bash
uv run uvicorn app.main:app --reload
```

The API will normally be available locally at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

OpenAPI alternative documentation:

```text
http://127.0.0.1:8000/redoc
```

## Code Quality

Format the application:

```bash
uv run ruff format app tests
```

Run linting:

```bash
uv run ruff check app tests
```

Run static type checking:

```bash
uv run mypy app
```

Run automated tests:

```bash
uv run pytest -v
```

## Security

Local environment files and databases are excluded from version control.

Examples include:

```text
.env
*.db
*.sqlite
*.sqlite3
.venv/
```

Sensitive healthcare information, credentials, API keys, and production patient data must never be committed to the repository.

> This project is currently a development and portfolio application. It should not be considered HIPAA-compliant or suitable for production handling of protected health information without additional security, privacy, auditing, infrastructure, and compliance controls.

## Roadmap

Planned development includes:

1. Complete Patient CRUD operations
2. Patient search and pagination
3. PostgreSQL integration
4. Authentication and authorization
5. Healthcare provider management
6. Appointment management
7. Clinical encounter APIs
8. Medical records architecture
9. Audit logging
10. Role-based access control
11. Docker containerization
12. CI/CD with GitHub Actions
13. AI-assisted clinical workflows
14. Healthcare RAG capabilities
15. AI agents for healthcare operations
16. Monitoring and observability
17. Production deployment architecture

## AI Vision

The long-term architecture is intended to support capabilities such as:

```text
Healthcare Data
      │
      ▼
MedTech APIs
      │
      ├── Patient Services
      ├── Provider Services
      ├── Appointment Services
      └── Clinical Services
      │
      ▼
AI / RAG Layer
      │
      ├── Healthcare Knowledge Retrieval
      ├── Document Intelligence
      ├── Clinical Workflow Assistance
      └── AI Agents
      │
      ▼
Healthcare Applications
```

The goal is to demonstrate how modern full-stack AI engineering practices can be applied to healthcare technology while maintaining clear boundaries between application services and AI capabilities.

## Disclaimer

This repository is intended for **software development, learning, demonstration, and portfolio purposes**.

It does not provide medical advice, diagnosis, or treatment and should not be used as a production clinical system without appropriate validation, security controls, regulatory review, and healthcare compliance measures.
