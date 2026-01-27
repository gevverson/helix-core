from pydantic import BaseModel
from typing import Optional, List
from app.domain.models import BloodGroup, Genotype, RiskLevel

# 1. Input Schema (What the Mobile App sends us)
class BioProfileCreate(BaseModel):
    blood_group: BloodGroup
    genotype: Genotype
    rhesus_factor: str  # We will parse this logic in the backend

# 2. Match Request Schema (Two people to check)
class MatchRequest(BaseModel):
    male_profile: BioProfileCreate
    female_profile: BioProfileCreate

# 3. Output Schema (What we send back)
class MatchResponse(BaseModel):
    status: RiskLevel
    messages: List[str]
    can_unblur_photos: bool
