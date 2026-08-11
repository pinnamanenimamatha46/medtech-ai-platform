## medtech-ai-platform
## Step 1 — Create the project folder:

    ##  mkdir medtech-ai-platform
    ## cd medtech-ai-platform

## Step 2 — Initialize the Python project
    ##  uv init --app --python 3.11

## Step 3 — Create the virtual environment
    ##  uv venv .venv --python 3.11
    ##  Actiivate it:   .venv\Scripts\activate

##  Step 4 -  Install the first backend dependencies
    ##  uv add fastapi uvicorn pydantic pydantic-settings sqlalchemy

    ##  uv sync

    ##  add development tools: 
    uv add --dev pytest pytest-asyncio httpx ruff mypy

##  Step 5 - erify installation
    
    ##  uv run python --version
    ## uv run ruff --version
    ## uv run pytest --version

## Step 6 - Create folders

    ##  New-Item -ItemType Directory -Force app
    ##  New-Item -ItemType Directory -Force app\api
    ##  New-Item -ItemType Directory -Force app\services
    ##  New-Item -ItemType Directory -Force app\models
    ##  New-Item -ItemType Directory -Force app\schemas
    ##  New-Item -ItemType Directory -Force app\core
    ##  New-Item -ItemType Directory -Force tests

##  Step 7  -   Create the Python package files:
    ## New-Item -ItemType File -Force app\__init__.py
    ##  New-Item -ItemType File -Force app\api\__init__.py
    ## New-Item -ItemType File -Force app\services\__init__.py
    ## New-Item -ItemType File -Force app\models\__init__.py
    ##  New-Item -ItemType File -Force app\schemas\__init__.py
    ##  New-Item -ItemType File -Force app\core\__init__.py
    ##  New-Item -ItemType File -Force app\main.py
    ##  New-Item -ItemType File -Force tests\test_health.py

##  Step 8 - Verify the structure   tree /F

##  Step 9 - Build the first FastAPI application

    ##  code app\main.py

"""Main FastAPI application for the MedTech AI Platform."""

from fastapi import FastAPI

app = FastAPI(
    title="MedTech AI Platform",
    description="AI-powered healthcare and medical technology platform.",
    version="0.1.0",
)


@app.get("/")
def root() -> dict[str, str]:
    """Return basic application information."""
    return {
        "name": "MedTech AI Platform",
        "status": "running",
    }


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    """Return application health status."""
    return {
        "status": "healthy",
    }

##  Step 10 - Start the API
    ##  uv run uvicorn app.main:app --reload
    ##  Uvicorn running on http://127.0.0.1:8000
    
    ##  open your browser and visit:    http://127.0.0.1:8000
        {"name":"MedTech AI Platform","status":"running"}
    
    ##  Test:   http://127.0.0.1:8000/api/v1/health
        {"status":"healthy"}
    
    ##  FastAPI Swagger documentation:
        http://127.0.0.1:8000/docs

##  Step 11 - Create the automated API tests
    ## code tests\test_health.py

"""Tests for the MedTech AI Platform health endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """Root endpoint should report that the platform is running."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "MedTech AI Platform",
        "status": "running",
    }


def test_health_endpoint() -> None:
    """Health endpoint should report healthy status."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }

## Step - 12 code pyproject.toml

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]

Step 13 - Run

    ## uv run ruff format app tests
    ## uv run ruff check app tests
    ## uv run mypy app
    ## uv run pytest -v ===2 passed, 1 warning in 0.55s======

## Step - 13 install `httpx2`
                ## uv add httpx2
                ## uv sync

## Step - 14 create the patient schema

    ## code app\schemas\patient.py

"""Patient schemas for the MedTech AI Platform."""

from datetime import date

from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    """Schema used when creating a patient."""

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    date_of_birth: date
    email: str | None = None
    phone: str | None = None


class PatientResponse(PatientCreate):
    """Schema returned by the patient API."""

    id: int

##  Step - 15   code app\schemas\__init__.py

"""Public schemas for the MedTech AI Platform."""

from app.schemas.patient import PatientCreate, PatientResponse

__all__ = [
    "PatientCreate",
    "PatientResponse",
]

##  Step - 16   Run
    
    ##  uv run ruff format app
    ##  uv run ruff check app
    ##  uv run mypy app

##  Step - 17   build the patient service layer.

    ## code app\services\patient_service.py

"""Patient service layer for the MedTech AI Platform."""

from app.schemas.patient import PatientCreate, PatientResponse


class PatientService:
    """Manage patient records in memory."""

    def __init__(self) -> None:
        self._patients: list[PatientResponse] = []
        self._next_id = 1

    def create_patient(self, patient: PatientCreate) -> PatientResponse:
        """Create and store a new patient."""
        created_patient = PatientResponse(
            id=self._next_id,
            **patient.model_dump(),
        )

        self._patients.append(created_patient)
        self._next_id += 1

        return created_patient

    def list_patients(self) -> list[PatientResponse]:
        """Return all patients."""
        return self._patients.copy()


patient_service = PatientService()

##  Step - 18   code app\services\__init__.py

"""Service layer for the MedTech AI Platform."""

from app.services.patient_service import PatientService, patient_service

__all__ = [
    "PatientService",
    "patient_service",
]

## Step - 19    Run
    ##  uv run ruff format app
    ##  uv run ruff check app
    ##  uv run mypy app

## Step - 20  Run
    ##  uv run uvicorn app,main:app
    ##  http://127.0.0.1:8000/docs 

##  Step - 21 create the Patient API

## code app\api\patients.py

"""Patient API routes for the MedTech AI Platform."""

from fastapi import APIRouter, status

from app.schemas.patient import PatientCreate, PatientResponse
from app.services.patient_service import patient_service

router = APIRouter(
    prefix="/api/v1/patients",
    tags=["patients"],
)


@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_patient(patient: PatientCreate) -> PatientResponse:
    """Create a patient."""
    return patient_service.create_patient(patient)


@router.get("", response_model=list[PatientResponse])
def list_patients() -> list[PatientResponse]:
    """Return all patients."""
    return patient_service.list_patients()

##  Step - 21   code app\main.py

"""Main FastAPI application for the MedTech AI Platform."""

from fastapi import FastAPI

from app.api.patients import router as patients_router

app = FastAPI(
    title="MedTech AI Platform",
    description="AI-powered healthcare and medical technology platform.",
    version="0.1.0",
)

app.include_router(patients_router)

##  Step - 22   Run
    ##  uv run ruff format app
    ##  uv run ruff check app
    ##  uv run mypy app

##  Step - 23   Test the Patient API in Swagger
    ##  http://127.0.0.1:8000/docs
        ##  POST  /api/v1/patients
            Try it out

{
  "first_name": "Anita",
  "last_name": "Kotha",
  "date_of_birth": "1970-10-15",
  "email": "anita.kotha@gmail.com",
  "phone": "840-217-5755"
}

Execute

Responses
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/patients' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Anita",
  "last_name": "Kotha",
  "date_of_birth": "1970-10-15",
  "email": "anita.kotha@gmail.com",
  "phone": "840-217-5755"
}

## Request URl http://127.0.0.1:8000/api/v1/patients

## 	
Response body
Download
{
  "first_name": "Anita",
  "last_name": "Kotha",
  "date_of_birth": "1970-10-15",
  "email": "anita.kotha@gmail.com",
  "phone": "840-217-5755",
  "id": 2
}

## 	Response body
Download
{
  "first_name": "Anita",
  "last_name": "Kotha",
  "date_of_birth": "1970-10-15",
  "email": "anita.kotha@gmail.com",
  "phone": "840-217-5755",
  "id": 2
}

##  Response headers
 content-length: 133 
 content-type: application/json 
 date: Tue,11 Aug 2026 03:01:37 GMT 
 server: uvicorn 

       ##  GET   /api/v1/patients

##  Step - 24   Add automated Patient API tests

    ##  code tests\test_patients.py

"""Tests for patient API endpoints."""

from fastapi.testclient import TestClient

from app.main import app
from app.services.patient_service import patient_service

client = TestClient(app)


def setup_function() -> None:
    """Reset the in-memory patient store before each test."""
    patient_service._patients.clear()
    patient_service._next_id = 1


def test_create_patient() -> None:
    """A patient should be created successfully."""
    response = client.post(
        "/api/v1/patients",
        json={
            "first_name": "Anita",
            "last_name": "Kotha",
            "date_of_birth": "1970-10-15",
            "email": "anita@example.com",
            "phone": "310-555-0101",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "first_name": "Anita",
        "last_name": "Kotha",
        "date_of_birth": "1970-10-15",
        "email": "anita@example.com",
        "phone": "310-555-0101",
        "id": 1,
    }


def test_list_patients() -> None:
    """Created patients should appear in the patient list."""
    client.post(
        "/api/v1/patients",
        json={
            "first_name": "Anita",
            "last_name": "Kotha",
            "date_of_birth": "1970-10-15",
            "email": "anita@example.com",
            "phone": "310-555-0101",
        },
    )

    response = client.get("/api/v1/patients")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["first_name"] == "Anita"
    assert response.json()[0]["id"] == 1

##  Step - 25   Run

    ##  uv run ruff format app tests
    ##  uv run ruff check app tests
    ##  uv run mypy app
    ##   uv run pytest -v   ====== 4 passed in 0.63s =====

## Replace the temporary in-memory patient list with a real SQLAlchemy database.

##  Step - 26   Create the database module
    ##  code app\core\database.py

"""Database configuration for the MedTech AI Platform."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "sqlite:///./medtech.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


def get_db() -> Generator[Session, None, None]:
    """Provide a database session."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

##  Step - 27   Create the Patient database model
    ##  code app\models\patient.py

"""Patient database model."""

from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Patient(Base):
    """Patient database record."""

    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

##  Step - 28   code app\models\__init__.py

"""Database models for the MedTech AI Platform."""

from app.models.patient import Patient

__all__ = [
    "Patient",
]

##  Step - 28   Verify this database foundation
    uv run ruff format app
    uv run ruff check app
    uv run mypy app

## connect the patient service to SQLite.

## Step - 29  Create the database tables on startup
    ##  code app\main.py

"""Main FastAPI application for the MedTech AI Platform."""

from fastapi import FastAPI

from app.api.patients import router as patients_router
from app.core.database import Base, engine

app = FastAPI(
    title="MedTech AI Platform",
    description="AI-powered healthcare and medical technology platform.",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(patients_router)

##  Step - 30   Replace the in-memory patient service

        ##  code app\services\patient_service.py

"""Patient service layer for the MedTech AI Platform."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientResponse


class PatientService:
    """Manage patient records using the database."""

    def create_patient(
        self,
        db: Session,
        patient: PatientCreate,
    ) -> PatientResponse:
        """Create and store a patient."""
        db_patient = Patient(
            first_name=patient.first_name,
            last_name=patient.last_name,
            date_of_birth=patient.date_of_birth,
            email=patient.email,
            phone=patient.phone,
        )

        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)

        return PatientResponse(
            id=db_patient.id,
            first_name=db_patient.first_name,
            last_name=db_patient.last_name,
            date_of_birth=db_patient.date_of_birth,
            email=db_patient.email,
            phone=db_patient.phone,
        )

    def list_patients(
        self,
        db: Session,
    ) -> list[PatientResponse]:
        """Return all patients."""
        statement = select(Patient).order_by(Patient.id)
        patients = db.scalars(statement).all()

        return [
            PatientResponse(
                id=patient.id,
                first_name=patient.first_name,
                last_name=patient.last_name,
                date_of_birth=patient.date_of_birth,
                email=patient.email,
                phone=patient.phone,
            )
            for patient in patients
        ]


patient_service = PatientService()

##  Step - 31   Update the patient API to use database sessions

``##    code app\api\patients.py
"""Patient API routes for the MedTech AI Platform."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.patient import PatientCreate, PatientResponse
from app.services.patient_service import patient_service

router = APIRouter(
    prefix="/api/v1/patients",
    tags=["patients"],
)


@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
) -> PatientResponse:
    """Create a patient."""
    return patient_service.create_patient(db, patient)


@router.get("", response_model=list[PatientResponse])
def list_patients(
    db: Session = Depends(get_db),
) -> list[PatientResponse]:
    """Return all patients."""
    return patient_service.list_patients(db)

## Step - 32 Run

uv run ruff format app
uv run ruff check app
uv run mypy app

##  Update the patient tests so they use a dedicated SQLite test database instead of the old in-memory reset.

##  Step - 33   code tests\test_patients.py

"""Tests for patient API endpoints."""

from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_medtech.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


def override_get_db() -> Generator[Session, None, None]:
    """Provide a test database session."""
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_function() -> None:
    """Reset the test database before each test."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


def test_create_patient() -> None:
    """A patient should be created successfully."""
    response = client.post(
        "/api/v1/patients",
        json={
            "first_name": "Anita",
            "last_name": "Kotha",
            "date_of_birth": "1970-10-15",
            "email": "anita@example.com",
            "phone": "310-555-0101",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "first_name": "Anita",
        "last_name": "Kotha",
        "date_of_birth": "1970-10-15",
        "email": "anita@example.com",
        "phone": "310-555-0101",
        "id": 1,
    }


def test_list_patients() -> None:
    """Created patients should appear in the patient list."""
    client.post(
        "/api/v1/patients",
        json={
            "first_name": "Anita",
            "last_name": "Kotha",
            "date_of_birth": "1970-10-15",
            "email": "anita@example.com",
            "phone": "310-555-0101",
        },
    )

    response = client.get("/api/v1/patients")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["first_name"] == "Anita"
    assert response.json()[0]["id"] == 1

##  Step - 34   Verify

uv run ruff format app tests
uv run ruff check app tests
uv run mypy app
uv run pytest -v    ==== 4 passed in 1.01s ======

##  Step - 35   code app\core\config.py








    





