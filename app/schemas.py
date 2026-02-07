from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional, List

# --- 1. BIOLOGICAL PROFILE ---
class BiologicalProfileBase(BaseModel):
    blood_group: str | None = None
    genotype: str | None = None
    rhesus_factor: str | None = None

class BiologicalProfileCreate(BiologicalProfileBase):
    pass

class BiologicalProfile(BiologicalProfileBase):
    id: UUID  # <--- FIXED: Changed from 'int' to 'UUID'
    
    class Config:
        from_attributes = True

# --- 2. USERS ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    full_name: str
    password: str
    bio_profile: BiologicalProfileCreate

class UserResponse(UserBase):
    id: UUID
    is_verified: bool
    bio_profile: BiologicalProfile | None = None 

    class Config:
        from_attributes = True

# --- 3. AUTHENTICATION ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class GoogleLoginRequest(BaseModel):
    token: str

# --- 4. MATCHING ---
class MatchRequest(BaseModel):
    male_profile: BiologicalProfileBase
    female_profile: BiologicalProfileBase

class MatchResponse(BaseModel):
    status: str
    messages: List[str]
    can_unblur_photos: bool

# --- 5. UPDATES ---
class ProfileUpdate(BaseModel):
    blood_group: str | None = None
    genotype: str | None = None
    rhesus_factor: str | None = None