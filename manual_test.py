from app.domain.models import BiologicalProfile, Genotype, BloodGroup
from app.domain.rules import check_compatibility

print("\n--- IRON GATE DIAGNOSTIC TEST ---")

# 1. Test Dangerous Match (AS + AS)
print("\n[TEST 1] Checking Sickle Cell Risk (AS + AS)...")
male = BiologicalProfile(genotype=Genotype.AS, rhesus_factor=BloodGroup.O_POS)
female = BiologicalProfile(genotype=Genotype.AS, rhesus_factor=BloodGroup.A_POS)
result = check_compatibility(male, female)

if result['status'] == 'danger':
    print("✅ SUCCESS: System correctly flagged RED LIGHT.")
    print(f"   Reason: {result['messages'][0]}")
else:
    print(f"❌ FAILED: Expected RED, got {result['status']}")

print("\n---------------------------------")
