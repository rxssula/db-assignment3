from database import engine, Base
from models import User, Caregiver, Member, Address, Job, JobApplication, Appointment

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()

