from app.domain.models import Genotype, BloodGroup, RiskLevel, BiologicalProfile

def check_compatibility(male_profile: BiologicalProfile, female_profile: BiologicalProfile) -> dict:
    """
    The Core 'Iron Gate' Logic.
    Compares two biological profiles and returns a Traffic Light risk assessment.
    """
    risk = RiskLevel.GREEN
    messages = []

    # --- RULE 1: SICKLE CELL / GENOTYPE CHECK (CRITICAL) ---
    male_g = male_profile.genotype
    female_g = female_profile.genotype

    if male_g and female_g:
        # If BOTH are NOT 'AA' (Normal), there is a risk.
        is_male_safe = male_g == Genotype.AA
        is_female_safe = female_g == Genotype.AA

        if not is_male_safe and not is_female_safe:
            risk = RiskLevel.RED
            messages.append(f"CRITICAL: Genetic incompatibility. Both partners carry traits ({male_g} + {female_g}). High risk of Sickle Cell Disease.")
        else:
            messages.append("Genotype compatibility: Safe.")

    # --- RULE 2: RHESUS FACTOR ---
    # Danger: Mother is Negative (-), Father is Positive (+)
    male_rh = male_profile.rhesus_factor
    female_rh = female_profile.rhesus_factor

    if male_rh and female_rh:
        if "NEG" in female_rh and "POS" in male_rh:
            if risk != RiskLevel.RED:
                risk = RiskLevel.AMBER
            messages.append("ADVISORY: Rhesus Incompatibility detected (Mother Rh- / Father Rh+).")

    return {
        "status": risk,
        "messages": messages
    }
