from sqlalchemy.orm import Session
from typing import List, Optional
from models import (
    User,
    Caregiver,
    Member,
    Address,
    Job,
    JobApplication,
    Appointment,
    GenderEnum,
    CaregivingTypeEnum,
    AppointmentStatusEnum
)
from schemas import (
    UserCreate, UserUpdate,
    CaregiverCreate, CaregiverUpdate,
    MemberCreate, MemberUpdate,
    AddressCreate, AddressUpdate,
    JobCreate, JobUpdate,
    JobApplicationCreate, JobApplicationUpdate,
    AppointmentCreate, AppointmentUpdate
)
import enum


def _convert_enum_value(value, enum_class):
    """Convert enum name or value to enum value string"""
    if value is None:
        return None
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, str):
        # Try to find by enum name first (e.g., "MALE" -> GenderEnum.MALE -> "Male")
        try:
            enum_member = getattr(enum_class, value.upper(), None)
            if enum_member and isinstance(enum_member, enum.Enum):
                return enum_member.value
        except (AttributeError, TypeError):
            pass
        # Try exact name match
        try:
            enum_member = getattr(enum_class, value, None)
            if enum_member and isinstance(enum_member, enum.Enum):
                return enum_member.value
        except (AttributeError, TypeError):
            pass
        # Try to find by value (case-insensitive)
        for e in enum_class:
            if e.value.lower() == value.lower() or e.value == value:
                return e.value
        # Try case-insensitive name match as last resort
        for e in enum_class:
            if e.name.upper() == value.upper():
                return e.value
    return value


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def create_caregiver(db: Session, caregiver: CaregiverCreate) -> Caregiver:
    # Use model_dump with mode='python' to get Python objects, then convert enums
    data = caregiver.model_dump(mode='python')
    # Convert enum names to values
    if 'gender' in data and data['gender'] is not None:
        data['gender'] = _convert_enum_value(data['gender'], GenderEnum)
    if 'caregiving_type' in data and data['caregiving_type'] is not None:
        data['caregiving_type'] = _convert_enum_value(data['caregiving_type'], CaregivingTypeEnum)
    db_caregiver = Caregiver(**data)
    db.add(db_caregiver)
    db.commit()
    db.refresh(db_caregiver)
    return db_caregiver


def get_caregiver(db: Session, caregiver_user_id: int) -> Optional[Caregiver]:
    return db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_user_id).first()


def get_caregivers(db: Session, skip: int = 0, limit: int = 100) -> List[Caregiver]:
    return db.query(Caregiver).offset(skip).limit(limit).all()


def update_caregiver(db: Session, caregiver_user_id: int, caregiver_update: CaregiverUpdate) -> Optional[Caregiver]:
    db_caregiver = get_caregiver(db, caregiver_user_id)
    if db_caregiver:
        update_data = caregiver_update.model_dump(exclude_unset=True, mode='python')
        # Convert enum names to values
        if 'gender' in update_data and update_data['gender'] is not None:
            update_data['gender'] = _convert_enum_value(update_data['gender'], GenderEnum)
        if 'caregiving_type' in update_data and update_data['caregiving_type'] is not None:
            update_data['caregiving_type'] = _convert_enum_value(update_data['caregiving_type'], CaregivingTypeEnum)
        for field, value in update_data.items():
            setattr(db_caregiver, field, value)
        db.commit()
        db.refresh(db_caregiver)
    return db_caregiver


def delete_caregiver(db: Session, caregiver_user_id: int) -> bool:
    db_caregiver = get_caregiver(db, caregiver_user_id)
    if db_caregiver:
        db.delete(db_caregiver)
        db.commit()
        return True
    return False


def create_member(db: Session, member: MemberCreate) -> Member:
    db_member = Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_member(db: Session, member_user_id: int) -> Optional[Member]:
    return db.query(Member).filter(Member.member_user_id == member_user_id).first()


def get_members(db: Session, skip: int = 0, limit: int = 100) -> List[Member]:
    return db.query(Member).offset(skip).limit(limit).all()


def update_member(db: Session, member_user_id: int, member_update: MemberUpdate) -> Optional[Member]:
    db_member = get_member(db, member_user_id)
    if db_member:
        update_data = member_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_member, field, value)
        db.commit()
        db.refresh(db_member)
    return db_member


def delete_member(db: Session, member_user_id: int) -> bool:
    db_member = get_member(db, member_user_id)
    if db_member:
        db.delete(db_member)
        db.commit()
        return True
    return False


def create_address(db: Session, address: AddressCreate) -> Address:
    db_address = Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address(db: Session, member_user_id: int) -> Optional[Address]:
    return db.query(Address).filter(Address.member_user_id == member_user_id).first()


def get_addresses(db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
    return db.query(Address).offset(skip).limit(limit).all()


def update_address(db: Session, member_user_id: int, address_update: AddressUpdate) -> Optional[Address]:
    db_address = get_address(db, member_user_id)
    if db_address:
        update_data = address_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_address, field, value)
        db.commit()
        db.refresh(db_address)
    return db_address


def delete_address(db: Session, member_user_id: int) -> bool:
    db_address = get_address(db, member_user_id)
    if db_address:
        db.delete(db_address)
        db.commit()
        return True
    return False


def create_job(db: Session, job: JobCreate) -> Job:
    data = job.model_dump(mode='python')
    # Convert enum names to values
    if 'required_caregiving_type' in data and data['required_caregiving_type'] is not None:
        data['required_caregiving_type'] = _convert_enum_value(data['required_caregiving_type'], CaregivingTypeEnum)
    db_job = Job(**data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_job(db: Session, job_id: int) -> Optional[Job]:
    return db.query(Job).filter(Job.job_id == job_id).first()


def get_jobs(db: Session, skip: int = 0, limit: int = 100) -> List[Job]:
    return db.query(Job).offset(skip).limit(limit).all()


def get_jobs_by_member(db: Session, member_user_id: int) -> List[Job]:
    return db.query(Job).filter(Job.member_user_id == member_user_id).all()


def update_job(db: Session, job_id: int, job_update: JobUpdate) -> Optional[Job]:
    db_job = get_job(db, job_id)
    if db_job:
        update_data = job_update.model_dump(exclude_unset=True, mode='python')
        # Convert enum names to values
        if 'required_caregiving_type' in update_data and update_data['required_caregiving_type'] is not None:
            update_data['required_caregiving_type'] = _convert_enum_value(update_data['required_caregiving_type'], CaregivingTypeEnum)
        for field, value in update_data.items():
            setattr(db_job, field, value)
        db.commit()
        db.refresh(db_job)
    return db_job


def delete_job(db: Session, job_id: int) -> bool:
    db_job = get_job(db, job_id)
    if db_job:
        db.delete(db_job)
        db.commit()
        return True
    return False


def create_job_application(db: Session, job_application: JobApplicationCreate) -> JobApplication:
    db_job_application = JobApplication(**job_application.model_dump())
    db.add(db_job_application)
    db.commit()
    db.refresh(db_job_application)
    return db_job_application


def get_job_application(db: Session, caregiver_user_id: int, job_id: int) -> Optional[JobApplication]:
    return db.query(JobApplication).filter(
        JobApplication.caregiver_user_id == caregiver_user_id,
        JobApplication.job_id == job_id
    ).first()


def get_job_applications(db: Session, skip: int = 0, limit: int = 100) -> List[JobApplication]:
    return db.query(JobApplication).offset(skip).limit(limit).all()


def get_job_applications_by_caregiver(db: Session, caregiver_user_id: int) -> List[JobApplication]:
    return db.query(JobApplication).filter(JobApplication.caregiver_user_id == caregiver_user_id).all()


def get_job_applications_by_job(db: Session, job_id: int) -> List[JobApplication]:
    return db.query(JobApplication).filter(JobApplication.job_id == job_id).all()


def update_job_application(db: Session, caregiver_user_id: int, job_id: int, job_application_update: JobApplicationUpdate) -> Optional[JobApplication]:
    db_job_application = get_job_application(db, caregiver_user_id, job_id)
    if db_job_application:
        update_data = job_application_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_job_application, field, value)
        db.commit()
        db.refresh(db_job_application)
    return db_job_application


def delete_job_application(db: Session, caregiver_user_id: int, job_id: int) -> bool:
    db_job_application = get_job_application(db, caregiver_user_id, job_id)
    if db_job_application:
        db.delete(db_job_application)
        db.commit()
        return True
    return False


def create_appointment(db: Session, appointment: AppointmentCreate) -> Appointment:
    data = appointment.model_dump(mode='python')
    if 'status' in data and data['status'] is not None:
        data['status'] = _convert_enum_value(data['status'], AppointmentStatusEnum)
    db_appointment = Appointment(**data)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointment(db: Session, appointment_id: int) -> Optional[Appointment]:
    return db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()


def get_appointments(db: Session, skip: int = 0, limit: int = 100) -> List[Appointment]:
    return db.query(Appointment).offset(skip).limit(limit).all()


def get_appointments_by_caregiver(db: Session, caregiver_user_id: int) -> List[Appointment]:
    return db.query(Appointment).filter(Appointment.caregiver_user_id == caregiver_user_id).all()


def get_appointments_by_member(db: Session, member_user_id: int) -> List[Appointment]:
    return db.query(Appointment).filter(Appointment.member_user_id == member_user_id).all()


def update_appointment(db: Session, appointment_id: int, appointment_update: AppointmentUpdate) -> Optional[Appointment]:
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment:
        update_data = appointment_update.model_dump(exclude_unset=True, mode='python')
        if 'status' in update_data and update_data['status'] is not None:
            update_data['status'] = _convert_enum_value(update_data['status'], AppointmentStatusEnum)
        for field, value in update_data.items():
            setattr(db_appointment, field, value)
        db.commit()
        db.refresh(db_appointment)
    return db_appointment


def delete_appointment(db: Session, appointment_id: int) -> bool:
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
        return True
    return False

