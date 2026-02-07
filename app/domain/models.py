import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class RiskLevel(str, Enum):
    GREEN = "safe"
    AMBER = "caution"
    RED = "danger"

class BloodGroup(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    O_POS = "O+"
    O_NEG = "O-"
    AB_POS = "AB+"
    AB_NEG = "AB-"

class Genotype(str, Enum):
    AA = "AA"
    AS = "AS"
    SS = "SS"
    AC = "AC"
    SC = "SC"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    # SECURITY UPDATE: The column below stores the encrypted hash, not the real password
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bio_profile = relationship("BiologicalProfile", back_populates="user", uselist=False)

class BiologicalProfile(Base):
    __tablename__ = "biological_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    
    blood_group = Column(String, nullable=True)
    genotype = Column(String, nullable=True)
    rhesus_factor = Column(String, nullable=True)
    raw_markers = Column(JSON, nullable=True)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="bio_profile")