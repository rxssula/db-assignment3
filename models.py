from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey, Text, Enum, TypeDecorator
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from database import Base
import enum


class GenderEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"


class CaregivingTypeEnum(str, enum.Enum):
    BABYSITTER = "Babysitter"
    ELDERLY_CARE = "ElderlyCare"
    PLAYMATE = "Playmate"


def _enum_values(enum_class):
    return [member.value for member in enum_class]


# Create PostgreSQL enum types that match the database
_base_gender_enum = PG_ENUM(
    GenderEnum,
    name="gender_enum",
    values_callable=_enum_values,
    validate_strings=True,
    create_type=False
)
_base_caregiving_type_enum = PG_ENUM(
    CaregivingTypeEnum,
    name="caregiving_type_enum",
    values_callable=_enum_values,
    validate_strings=True,
    create_type=False
)


def _normalize_enum_value(value, enum_class):
    """Convert different enum representations to the canonical DB value."""
    if value is None:
        return None
    if isinstance(value, enum.Enum):
        # If it's already the right enum class, return its value
        if isinstance(value, enum_class):
            return value.value
        # Try matching by name in case it's a different enum subclass
        try:
            return enum_class[value.name].value
        except (AttributeError, KeyError):
            pass
    if isinstance(value, str):
        candidate = value.strip()
        if not candidate:
            return None
        # Match by enum name (case-insensitive)
        try:
            return enum_class[candidate.upper()].value
        except KeyError:
            pass
        # Match by enum value (case-insensitive)
        for member in enum_class:
            if member.value.lower() == candidate.lower():
                return member.value
    raise ValueError(f"Invalid value '{value}' for enum {enum_class.__name__}")


class EnumValueType(TypeDecorator):
    """TypeDecorator that ensures enum values (not names) are stored"""
    impl = String
    cache_ok = True
    
    def __init__(self, enum_class, base_enum_type, *args, **kwargs):
        self.enum_class = enum_class
        self.base_enum_type = base_enum_type
        super().__init__(*args, **kwargs)
    
    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(self.base_enum_type)
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return _normalize_enum_value(value, self.enum_class)
    
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        # Convert string value back to enum
        if isinstance(value, enum.Enum):
            return value
        if isinstance(value, str):
            for e in self.enum_class:
                if e.value == value:
                    return e
        return value


# Create enum types with value conversion
gender_enum = EnumValueType(GenderEnum, _base_gender_enum)
caregiving_type_enum = EnumValueType(CaregivingTypeEnum, _base_caregiving_type_enum)


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
    gender = Column(gender_enum)
    caregiving_type = Column(caregiving_type_enum)
    hourly_rate = Column(Float)
    
    user = relationship("User", back_populates="caregiver")
    job_applications = relationship("JobApplication", back_populates="caregiver")
    appointments = relationship("Appointment", back_populates="caregiver")

    @validates("gender")
    def _validate_gender(self, key, value):
        return _normalize_enum_value(value, GenderEnum)

    @validates("caregiving_type")
    def _validate_caregiving_type(self, key, value):
        return _normalize_enum_value(value, CaregivingTypeEnum)


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
    required_caregiving_type = Column(caregiving_type_enum)
    other_requirements = Column(Text)
    date_posted = Column(Date)
    
    member = relationship("Member", back_populates="jobs")
    job_applications = relationship("JobApplication", back_populates="job")

    @validates("required_caregiving_type")
    def _validate_required_caregiving_type(self, key, value):
        return _normalize_enum_value(value, CaregivingTypeEnum)


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

