import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

# 1. The Base Class (The foundation for all tables)
Base = declarative_base()

# 2. Enums (Strict Rules - No typos allowed in medical data)
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
    AA = "AA"  # Normal
    AS = "AS"  # Sickle Cell Carrier
    SS = "SS"  # Sickle Cell Anaemia
    AC = "AC"  # Carrier
    SC = "SC"  # Disease

# 3. The User Table (Identity Vault)
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # True only if medicals are checked
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship: One User has One Biological Profile
    bio_profile = relationship("BiologicalProfile", back_populates="user", uselist=False)

# 4. The Biological Profile (The Bio-Core)
class BiologicalProfile(Base):
    __tablename__ = "biological_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    
    # Core Medical Data
    blood_group = Column(String, nullable=True) # Stored as Enum string
    genotype = Column(String, nullable=True)    # Stored as Enum string
    rhesus_factor = Column(String, nullable=True) 
    
    # Advanced: Store raw genetic markers (HLA, etc.) in a JSON blob for flexibility
    raw_markers = Column(JSON, nullable=True)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship back to User
    user = relationship("User", back_populates="bio_profile")