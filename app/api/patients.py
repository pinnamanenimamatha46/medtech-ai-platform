"""Patient API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.patient import PatientCreate, PatientResponse
from app.services.patient_service import patient_service

router = APIRouter(prefix="/patients", tags=["patients"])

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_patient(
    patient_data: PatientCreate,
    db: DatabaseSession,
) -> PatientResponse:
    """Create a new patient."""
    patient = patient_service.create_patient(db, patient_data)

    return PatientResponse.model_validate(patient)


@router.get(
    "",
    response_model=list[PatientResponse],
)
def list_patients(
    db: DatabaseSession,
    skip: int = 0,
    limit: int = 100,
) -> list[PatientResponse]:
    """Return all patients."""
    patients = patient_service.list_patients(
        db,
        skip=skip,
        limit=limit,
    )

    return [PatientResponse.model_validate(patient) for patient in patients]


@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
)
def get_patient(
    patient_id: int,
    db: DatabaseSession,
) -> PatientResponse:
    """Return a patient by ID."""
    patient = patient_service.get_patient(db, patient_id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    return PatientResponse.model_validate(patient)
