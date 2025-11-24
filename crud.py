from sqlalchemy.orm import Session
from typing import List, Optional
from models import User, Caregiver, Member, Address, Job, JobApplication, Appointment
from schemas import (
    UserCreate, UserUpdate,
    CaregiverCreate, CaregiverUpdate,
    MemberCreate, MemberUpdate,
    AddressCreate, AddressUpdate,
    JobCreate, JobUpdate,
    JobApplicationCreate, JobApplicationUpdate,
    AppointmentCreate, AppointmentUpdate
)


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
    db_caregiver = Caregiver(**caregiver.model_dump())
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
        update_data = caregiver_update.model_dump(exclude_unset=True)
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
    db_job = Job(**job.model_dump())
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
        update_data = job_update.model_dump(exclude_unset=True)
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
    db_appointment = Appointment(**appointment.model_dump())
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
        update_data = appointment_update.model_dump(exclude_unset=True)
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

