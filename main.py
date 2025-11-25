from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from database import get_db, engine
from db_utils import ensure_appointment_status_constraint
from schemas import (
    UserCreate, UserUpdate, UserResponse,
    CaregiverCreate, CaregiverUpdate, CaregiverResponse,
    MemberCreate, MemberUpdate, MemberResponse,
    AddressCreate, AddressUpdate, AddressResponse,
    JobCreate, JobUpdate, JobResponse,
    JobApplicationCreate, JobApplicationUpdate, JobApplicationResponse,
    AppointmentCreate, AppointmentUpdate, AppointmentResponse
)
import crud

app = FastAPI(title="Caregiver Management API", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    import time
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            ensure_appointment_status_constraint(engine)
            print("Database connection established successfully!")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Database connection failed (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print(f"Warning: Could not establish initial database connection: {e}")
                print("The database may be sleeping. Connections will be retried on first request.")


@app.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/caregivers/", response_model=CaregiverResponse, status_code=201)
def create_caregiver(caregiver: CaregiverCreate, db: Session = Depends(get_db)):
    return crud.create_caregiver(db=db, caregiver=caregiver)


@app.get("/caregivers/", response_model=List[CaregiverResponse])
def read_caregivers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    caregivers = crud.get_caregivers(db, skip=skip, limit=limit)
    return caregivers


@app.get("/caregivers/{caregiver_user_id}", response_model=CaregiverResponse)
def read_caregiver(caregiver_user_id: int, db: Session = Depends(get_db)):
    db_caregiver = crud.get_caregiver(db, caregiver_user_id=caregiver_user_id)
    if db_caregiver is None:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    return db_caregiver


@app.put("/caregivers/{caregiver_user_id}", response_model=CaregiverResponse)
def update_caregiver(caregiver_user_id: int, caregiver: CaregiverUpdate, db: Session = Depends(get_db)):
    db_caregiver = crud.update_caregiver(db, caregiver_user_id=caregiver_user_id, caregiver_update=caregiver)
    if db_caregiver is None:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    return db_caregiver


@app.delete("/caregivers/{caregiver_user_id}", status_code=204)
def delete_caregiver(caregiver_user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_caregiver(db, caregiver_user_id=caregiver_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Caregiver not found")


@app.post("/members/", response_model=MemberResponse, status_code=201)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    return crud.create_member(db=db, member=member)


@app.get("/members/", response_model=List[MemberResponse])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = crud.get_members(db, skip=skip, limit=limit)
    return members


@app.get("/members/{member_user_id}", response_model=MemberResponse)
def read_member(member_user_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_user_id=member_user_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@app.put("/members/{member_user_id}", response_model=MemberResponse)
def update_member(member_user_id: int, member: MemberUpdate, db: Session = Depends(get_db)):
    db_member = crud.update_member(db, member_user_id=member_user_id, member_update=member)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@app.delete("/members/{member_user_id}", status_code=204)
def delete_member(member_user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_member(db, member_user_id=member_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")


@app.post("/addresses/", response_model=AddressResponse, status_code=201)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address(db=db, address=address)


@app.get("/addresses/", response_model=List[AddressResponse])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db, skip=skip, limit=limit)
    return addresses


@app.get("/addresses/{member_user_id}", response_model=AddressResponse)
def read_address(member_user_id: int, db: Session = Depends(get_db)):
    db_address = crud.get_address(db, member_user_id=member_user_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.put("/addresses/{member_user_id}", response_model=AddressResponse)
def update_address(member_user_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    db_address = crud.update_address(db, member_user_id=member_user_id, address_update=address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.delete("/addresses/{member_user_id}", status_code=204)
def delete_address(member_user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_address(db, member_user_id=member_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")


@app.post("/jobs/", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db=db, job=job)


@app.get("/jobs/", response_model=List[JobResponse])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs


@app.get("/jobs/{job_id}", response_model=JobResponse)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job


@app.get("/jobs/member/{member_user_id}", response_model=List[JobResponse])
def read_jobs_by_member(member_user_id: int, db: Session = Depends(get_db)):
    jobs = crud.get_jobs_by_member(db, member_user_id=member_user_id)
    return jobs


@app.put("/jobs/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    db_job = crud.update_job(db, job_id=job_id, job_update=job)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job


@app.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    success = crud.delete_job(db, job_id=job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")


@app.post("/job-applications/", response_model=JobApplicationResponse, status_code=201)
def create_job_application(job_application: JobApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_job_application(db=db, job_application=job_application)


@app.get("/job-applications/", response_model=List[JobApplicationResponse])
def read_job_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job_applications = crud.get_job_applications(db, skip=skip, limit=limit)
    return job_applications


@app.get("/job-applications/caregiver/{caregiver_user_id}", response_model=List[JobApplicationResponse])
def read_job_applications_by_caregiver(caregiver_user_id: int, db: Session = Depends(get_db)):
    job_applications = crud.get_job_applications_by_caregiver(db, caregiver_user_id=caregiver_user_id)
    return job_applications


@app.get("/job-applications/job/{job_id}", response_model=List[JobApplicationResponse])
def read_job_applications_by_job(job_id: int, db: Session = Depends(get_db)):
    job_applications = crud.get_job_applications_by_job(db, job_id=job_id)
    return job_applications


@app.get("/job-applications/{caregiver_user_id}/{job_id}", response_model=JobApplicationResponse)
def read_job_application(caregiver_user_id: int, job_id: int, db: Session = Depends(get_db)):
    db_job_application = crud.get_job_application(db, caregiver_user_id=caregiver_user_id, job_id=job_id)
    if db_job_application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    return db_job_application


@app.put("/job-applications/{caregiver_user_id}/{job_id}", response_model=JobApplicationResponse)
def update_job_application(caregiver_user_id: int, job_id: int, job_application: JobApplicationUpdate, db: Session = Depends(get_db)):
    db_job_application = crud.update_job_application(db, caregiver_user_id=caregiver_user_id, job_id=job_id, job_application_update=job_application)
    if db_job_application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    return db_job_application


@app.delete("/job-applications/{caregiver_user_id}/{job_id}", status_code=204)
def delete_job_application(caregiver_user_id: int, job_id: int, db: Session = Depends(get_db)):
    success = crud.delete_job_application(db, caregiver_user_id=caregiver_user_id, job_id=job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job application not found")


@app.post("/appointments/", response_model=AppointmentResponse, status_code=201)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db=db, appointment=appointment)


@app.get("/appointments/", response_model=List[AppointmentResponse])
def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = crud.get_appointments(db, skip=skip, limit=limit)
    return appointments


@app.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = crud.get_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment


@app.get("/appointments/caregiver/{caregiver_user_id}", response_model=List[AppointmentResponse])
def read_appointments_by_caregiver(caregiver_user_id: int, db: Session = Depends(get_db)):
    appointments = crud.get_appointments_by_caregiver(db, caregiver_user_id=caregiver_user_id)
    return appointments


@app.get("/appointments/member/{member_user_id}", response_model=List[AppointmentResponse])
def read_appointments_by_member(member_user_id: int, db: Session = Depends(get_db)):
    appointments = crud.get_appointments_by_member(db, member_user_id=member_user_id)
    return appointments


@app.put("/appointments/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(appointment_id: int, appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    db_appointment = crud.update_appointment(db, appointment_id=appointment_id, appointment_update=appointment)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment


@app.delete("/appointments/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    success = crud.delete_appointment(db, appointment_id=appointment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Appointment not found")


@app.get("/")
def root():
    return {"message": "Welcome to the Caregiver Management API"}

