from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, time


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
    gender: Optional[str] = None
    caregiving_type: Optional[str] = None
    hourly_rate: Optional[float] = None


class CaregiverCreate(CaregiverBase):
    caregiver_user_id: int


class CaregiverUpdate(BaseModel):
    photo: Optional[str] = None
    gender: Optional[str] = None
    caregiving_type: Optional[str] = None
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
    required_caregiving_type: Optional[str] = None
    other_requirements: Optional[str] = None
    date_posted: Optional[date] = None


class JobCreate(JobBase):
    member_user_id: int


class JobUpdate(BaseModel):
    member_user_id: Optional[int] = None
    required_caregiving_type: Optional[str] = None
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
    status: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    caregiver_user_id: int
    member_user_id: int


class AppointmentUpdate(BaseModel):
    caregiver_user_id: Optional[int] = None
    member_user_id: Optional[int] = None
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    work_hours: Optional[float] = None
    status: Optional[str] = None


class AppointmentResponse(AppointmentBase):
    appointment_id: int
    caregiver_user_id: int
    member_user_id: int
    
    class Config:
        from_attributes = True

