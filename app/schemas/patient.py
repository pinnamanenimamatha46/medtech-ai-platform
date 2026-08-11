"""Patient schemas."""

from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class PatientCreate(BaseModel):
    """Schema for creating a patient."""

    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone: str


class PatientResponse(BaseModel):
    """Schema returned for patient API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone: str
