from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date, time
from models import GenderEnum, CaregivingTypeEnum, AppointmentStatusEnum
import enum


def _coerce_enum(value, enum_class):
    """Allow API clients to send enum names (e.g., MALE) or values (e.g., Male)."""
    if value is None or isinstance(value, enum_class):
        return value
    if isinstance(value, enum.Enum):
        try:
            return enum_class[value.name]
        except KeyError:
            pass
    if isinstance(value, str):
        candidate = value.strip()
        if not candidate:
            return None
        try:
            return enum_class[candidate.upper()]
        except KeyError:
            pass
        for member in enum_class:
            if member.value.lower() == candidate.lower():
                return member
    raise ValueError(f"Invalid value '{value}' for enum {enum_class.__name__}")


class UserBase(BaseModel):
    email: EmailStr
    given_name: str
    surname: str
    city: Optional[str] = None
    phone_number: Optional[str] = None
    profile_description: Optional[str] = None
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    given_name: Optional[str] = None
    surname: Optional[str] = None
    city: Optional[str] = None
    phone_number: Optional[str] = None
    profile_description: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    user_id: int
    
    class Config:
        from_attributes = True


class CaregiverBase(BaseModel):
    photo: Optional[str] = None
    gender: Optional[GenderEnum] = None
    caregiving_type: Optional[CaregivingTypeEnum] = None
    hourly_rate: Optional[float] = None

    @field_validator("gender", mode="before")
    @classmethod
    def _normalize_gender(cls, value):
        return _coerce_enum(value, GenderEnum)

    @field_validator("caregiving_type", mode="before")
    @classmethod
    def _normalize_caregiving_type(cls, value):
        return _coerce_enum(value, CaregivingTypeEnum)


class CaregiverCreate(CaregiverBase):
    caregiver_user_id: int


class CaregiverUpdate(BaseModel):
    photo: Optional[str] = None
    gender: Optional[GenderEnum] = None
    caregiving_type: Optional[CaregivingTypeEnum] = None
    hourly_rate: Optional[float] = None


class CaregiverResponse(CaregiverBase):
    caregiver_user_id: int
    
    class Config:
        from_attributes = True


class MemberBase(BaseModel):
    house_rules: Optional[str] = None
    dependent_description: Optional[str] = None


class MemberCreate(MemberBase):
    member_user_id: int


class MemberUpdate(BaseModel):
    house_rules: Optional[str] = None
    dependent_description: Optional[str] = None


class MemberResponse(MemberBase):
    member_user_id: int
    
    class Config:
        from_attributes = True


class AddressBase(BaseModel):
    house_number: Optional[str] = None
    street: Optional[str] = None
    town: Optional[str] = None


class AddressCreate(AddressBase):
    member_user_id: int


class AddressUpdate(BaseModel):
    house_number: Optional[str] = None
    street: Optional[str] = None
    town: Optional[str] = None


class AddressResponse(AddressBase):
    member_user_id: int
    
    class Config:
        from_attributes = True


class JobBase(BaseModel):
    required_caregiving_type: Optional[CaregivingTypeEnum] = None
    other_requirements: Optional[str] = None
    date_posted: Optional[date] = None

    @field_validator("required_caregiving_type", mode="before")
    @classmethod
    def _normalize_required_caregiving_type(cls, value):
        return _coerce_enum(value, CaregivingTypeEnum)


class JobCreate(JobBase):
    member_user_id: int


class JobUpdate(BaseModel):
    member_user_id: Optional[int] = None
    required_caregiving_type: Optional[CaregivingTypeEnum] = None
    other_requirements: Optional[str] = None
    date_posted: Optional[date] = None


class JobResponse(JobBase):
    job_id: int
    member_user_id: int
    
    class Config:
        from_attributes = True


class JobApplicationBase(BaseModel):
    date_applied: Optional[date] = None


class JobApplicationCreate(JobApplicationBase):
    caregiver_user_id: int
    job_id: int


class JobApplicationUpdate(BaseModel):
    date_applied: Optional[date] = None


class JobApplicationResponse(JobApplicationBase):
    caregiver_user_id: int
    job_id: int
    
    class Config:
        from_attributes = True


class AppointmentBase(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    work_hours: Optional[float] = None
    status: Optional[AppointmentStatusEnum] = None

    @field_validator("status", mode="before")
    @classmethod
    def _normalize_status(cls, value):
        return _coerce_enum(value, AppointmentStatusEnum)


class AppointmentCreate(AppointmentBase):
    caregiver_user_id: int
    member_user_id: int


class AppointmentUpdate(BaseModel):
    caregiver_user_id: Optional[int] = None
    member_user_id: Optional[int] = None
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    work_hours: Optional[float] = None
    status: Optional[AppointmentStatusEnum] = None


class AppointmentResponse(AppointmentBase):
    appointment_id: int
    caregiver_user_id: int
    member_user_id: int
    
    class Config:
        from_attributes = True

