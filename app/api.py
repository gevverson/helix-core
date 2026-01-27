from fastapi import FastAPI
from app.schemas import MatchRequest, MatchResponse
from app.domain.models import BiologicalProfile
from app.domain.rules import check_compatibility

app = FastAPI(title="The Iron Gate API", version="1.0.0")

@app.post("/check-match", response_model=MatchResponse)
def check_match_compatibility(request: MatchRequest):
    """
    Evaluates genetic compatibility between two profiles.
    Returns: GREEN (Safe), AMBER (Caution), or RED (Danger).
    """
    # 1. Convert API data to Internal Domain Models
    male = BiologicalProfile(
        genotype=request.male_profile.genotype,
        rhesus_factor=request.male_profile.rhesus_factor
    )
    female = BiologicalProfile(
        genotype=request.female_profile.genotype,
        rhesus_factor=request.female_profile.rhesus_factor
    )

    # 2. Run the Rules Engine
    result = check_compatibility(male, female)

    # 3. Determine if photos can be unblurred
    can_unblur = result["status"] != "danger"

    return MatchResponse(
        status=result["status"],
        messages=result["messages"],
        can_unblur_photos=can_unblur
    )
