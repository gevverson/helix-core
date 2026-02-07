import pytesseract
from PIL import Image
import io

def read_medical_report(image_bytes: bytes) -> dict:
    """
    Takes a raw image file, reads the text, and hunts for keywords.
    """
    # 1. Open the image from memory
    image = Image.open(io.BytesIO(image_bytes))
    
    # 2. Extract ALL text
    raw_text = pytesseract.image_to_string(image)
    
    # 3. Clean the text (convert to uppercase for easier matching)
    clean_text = raw_text.upper()
    
    # 4. Search for Medical Keywords (The "Parser")
    result = {
        "genotype": None,
        "blood_group": None,
        "raw_text": raw_text[0:500] + "..." # Store first 500 chars for debugging
    }

    # --- GENOTYPE LOGIC ---
    if "AA" in clean_text: result["genotype"] = "AA"
    elif "AS" in clean_text: result["genotype"] = "AS"
    elif "SS" in clean_text: result["genotype"] = "SS"
    elif "AC" in clean_text: result["genotype"] = "AC"
    elif "SC" in clean_text: result["genotype"] = "SC"

    # --- BLOOD GROUP LOGIC ---
    # We check specific patterns. Order matters (Check AB before A or B)
    if "O+" in clean_text or "O POS" in clean_text: result["blood_group"] = "O+"
    elif "O-" in clean_text or "O NEG" in clean_text: result["blood_group"] = "O-"
    elif "AB+" in clean_text or "AB POS" in clean_text: result["blood_group"] = "AB+"
    elif "AB-" in clean_text or "AB NEG" in clean_text: result["blood_group"] = "AB-"
    elif "A+" in clean_text or "A POS" in clean_text: result["blood_group"] = "A+"
    elif "A-" in clean_text or "A NEG" in clean_text: result["blood_group"] = "A-"
    elif "B+" in clean_text or "B POS" in clean_text: result["blood_group"] = "B+"
    elif "B-" in clean_text or "B NEG" in clean_text: result["blood_group"] = "B-"

    return result