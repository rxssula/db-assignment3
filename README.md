# Caregiver Management API

A FastAPI-based REST API for managing caregivers, members, jobs, applications, and appointments.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

**If you encounter wheel build errors** (especially on macOS), try one of these solutions:

**Option 1: Install PostgreSQL development libraries (macOS)**
```bash
brew install postgresql
pip install -r requirements.txt
```

**Option 2: Use psycopg3 instead (alternative driver)**
```bash
pip install -r requirements_alternative.txt
```

**Option 3: Use a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

2. The database URL is already configured in `config.py` (defaults to your provided URL).

3. Initialize database tables (if needed):
```bash
python init_db.py
```

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## Database Tables

- **USER**: Basic user information
- **CAREGIVER**: Caregiver-specific details
- **MEMBER**: Member-specific details
- **ADDRESS**: Member addresses
- **JOB**: Job postings
- **JOB_APPLICATION**: Job applications by caregivers
- **APPOINTMENT**: Scheduled appointments

## API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get a specific user
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Delete a user

### Caregivers
- `POST /caregivers/` - Create a new caregiver
- `GET /caregivers/` - List all caregivers
- `GET /caregivers/{caregiver_user_id}` - Get a specific caregiver
- `PUT /caregivers/{caregiver_user_id}` - Update a caregiver
- `DELETE /caregivers/{caregiver_user_id}` - Delete a caregiver

### Members
- `POST /members/` - Create a new member
- `GET /members/` - List all members
- `GET /members/{member_user_id}` - Get a specific member
- `PUT /members/{member_user_id}` - Update a member
- `DELETE /members/{member_user_id}` - Delete a member

### Addresses
- `POST /addresses/` - Create a new address
- `GET /addresses/` - List all addresses
- `GET /addresses/{member_user_id}` - Get address for a member
- `PUT /addresses/{member_user_id}` - Update an address
- `DELETE /addresses/{member_user_id}` - Delete an address

### Jobs
- `POST /jobs/` - Create a new job
- `GET /jobs/` - List all jobs
- `GET /jobs/{job_id}` - Get a specific job
- `GET /jobs/member/{member_user_id}` - Get jobs by member
- `PUT /jobs/{job_id}` - Update a job
- `DELETE /jobs/{job_id}` - Delete a job

### Job Applications
- `POST /job-applications/` - Create a new job application
- `GET /job-applications/` - List all job applications
- `GET /job-applications/{caregiver_user_id}/{job_id}` - Get a specific application
- `GET /job-applications/caregiver/{caregiver_user_id}` - Get applications by caregiver
- `GET /job-applications/job/{job_id}` - Get applications for a job
- `PUT /job-applications/{caregiver_user_id}/{job_id}` - Update an application
- `DELETE /job-applications/{caregiver_user_id}/{job_id}` - Delete an application

### Appointments
- `POST /appointments/` - Create a new appointment
- `GET /appointments/` - List all appointments
- `GET /appointments/{appointment_id}` - Get a specific appointment
- `GET /appointments/caregiver/{caregiver_user_id}` - Get appointments by caregiver
- `GET /appointments/member/{member_user_id}` - Get appointments by member
- `PUT /appointments/{appointment_id}` - Update an appointment
- `DELETE /appointments/{appointment_id}` - Delete an appointment

