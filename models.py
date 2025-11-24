from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "user"
    
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    given_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    city = Column(String)
    phone_number = Column(String)
    profile_description = Column(Text)
    password = Column(String, nullable=False)
    
    caregiver = relationship("Caregiver", back_populates="user", uselist=False)
    member = relationship("Member", back_populates="user", uselist=False)


class Caregiver(Base):
    __tablename__ = "caregiver"
    
    caregiver_user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True, index=True)
    photo = Column(String)
    gender = Column(String)
    caregiving_type = Column(String)
    hourly_rate = Column(Float)
    
    user = relationship("User", back_populates="caregiver")
    job_applications = relationship("JobApplication", back_populates="caregiver")
    appointments = relationship("Appointment", back_populates="caregiver")


class Member(Base):
    __tablename__ = "member"
    
    member_user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True, index=True)
    house_rules = Column(Text)
    dependent_description = Column(Text)
    
    user = relationship("User", back_populates="member")
    address = relationship("Address", back_populates="member", uselist=False)
    jobs = relationship("Job", back_populates="member")
    appointments = relationship("Appointment", back_populates="member")


class Address(Base):
    __tablename__ = "address"
    
    member_user_id = Column(Integer, ForeignKey("member.member_user_id"), primary_key=True, index=True)
    house_number = Column(String)
    street = Column(String)
    town = Column(String)
    
    member = relationship("Member", back_populates="address")


class Job(Base):
    __tablename__ = "job"
    
    job_id = Column(Integer, primary_key=True, index=True)
    member_user_id = Column(Integer, ForeignKey("member.member_user_id"), nullable=False)
    required_caregiving_type = Column(String)
    other_requirements = Column(Text)
    date_posted = Column(Date)
    
    member = relationship("Member", back_populates="jobs")
    job_applications = relationship("JobApplication", back_populates="job")


class JobApplication(Base):
    __tablename__ = "job_application"
    
    caregiver_user_id = Column(Integer, ForeignKey("caregiver.caregiver_user_id"), primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job.job_id"), primary_key=True, index=True)
    date_applied = Column(Date)
    
    caregiver = relationship("Caregiver", back_populates="job_applications")
    job = relationship("Job", back_populates="job_applications")


class Appointment(Base):
    __tablename__ = "appointment"
    
    appointment_id = Column(Integer, primary_key=True, index=True)
    caregiver_user_id = Column(Integer, ForeignKey("caregiver.caregiver_user_id"), nullable=False)
    member_user_id = Column(Integer, ForeignKey("member.member_user_id"), nullable=False)
    appointment_date = Column(Date)
    appointment_time = Column(Time)
    work_hours = Column(Float)
    status = Column(String)
    
    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")

