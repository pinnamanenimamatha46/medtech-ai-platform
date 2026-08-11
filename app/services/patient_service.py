"""Service layer for patient operations."""

from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientCreate


class PatientService:
    """Service for managing patient records."""

    def create_patient(
        self,
        db: Session,
        patient_data: PatientCreate,
    ) -> Patient:
        """Create and persist a new patient."""
        patient = Patient(**patient_data.model_dump())

        db.add(patient)
        db.commit()
        db.refresh(patient)

        return patient

    def get_patient(
        self,
        db: Session,
        patient_id: int,
    ) -> Patient | None:
        """Retrieve a patient by ID."""
        return db.get(Patient, patient_id)

    def list_patients(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Patient]:
        """Return a paginated list of patients."""
        return db.query(Patient).offset(skip).limit(limit).all()

    def update_patient(
        self,
        db: Session,
        patient: Patient,
        patient_data: PatientCreate,
    ) -> Patient:
        """Update an existing patient."""
        update_data = patient_data.model_dump()

        for field, value in update_data.items():
            setattr(patient, field, value)

        db.add(patient)
        db.commit()
        db.refresh(patient)

        return patient

    def delete_patient(
        self,
        db: Session,
        patient: Patient,
    ) -> None:
        """Delete an existing patient."""
        db.delete(patient)
        db.commit()


patient_service = PatientService()
