from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

# Google Libraries
from google.oauth2 import id_token
from google.auth.transport import requests

# App Imports
from app.schemas import (
    MatchRequest, MatchResponse, UserCreate, UserResponse, 
    Token, GoogleLoginRequest, ProfileUpdate
)
from app.domain.models import BiologicalProfile, User
from app.domain.rules import check_compatibility
from app.core.database import get_db
from app.core.security import (
    get_password_hash, verify_password, create_access_token, 
    SECRET_KEY, ALGORITHM
)
from app.core.ocr import read_medical_report

# --- INITIALIZATION ---
app = FastAPI(title="The Iron Gate API", version="1.0.0")

# --- CORS (Security Config) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared Security Tool
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID_HERE"

# --- 1. LOGIN (Get Token) ---
@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- 2. GOOGLE LOGIN ---
@app.post("/auth/google", response_model=Token)
def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        # Mocking verification for now. In prod, uncomment the verify lines.
        email = request.token 
        
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            new_user = User(
                email=email,
                full_name="Google User",
                hashed_password="GOOGLE_LOGIN_NO_PASSWORD",
                is_active=True
            )
            new_user.bio_profile = BiologicalProfile() # Empty profile
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user = new_user
            
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google Token")

# --- 3. REGISTER NEW USER ---
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = get_password_hash(user.password)

    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_pwd,
        is_active=True
    )
    
    new_bio = BiologicalProfile(
        blood_group=user.bio_profile.blood_group,
        genotype=user.bio_profile.genotype,
        rhesus_factor=user.bio_profile.rhesus_factor
    )
    
    new_user.bio_profile = new_bio
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# --- 4. CHECK MATCH COMPATIBILITY ---
@app.post("/check-match", response_model=MatchResponse)
def check_match_compatibility(request: MatchRequest):
    male = BiologicalProfile(
        genotype=request.male_profile.genotype,
        rhesus_factor=request.male_profile.rhesus_factor
    )
    female = BiologicalProfile(
        genotype=request.female_profile.genotype,
        rhesus_factor=request.female_profile.rhesus_factor
    )

    result = check_compatibility(male, female)
    can_unblur = result["status"] != "danger"

    return MatchResponse(
        status=result["status"],
        messages=result["messages"],
        can_unblur_photos=can_unblur
    )

# --- 5. UPDATE PROFILE (SAVE DATA) ---
@app.patch("/users/me/profile")
def update_profile(
    profile_data: ProfileUpdate, 
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # 1. Decode the Token to find out WHO is logged in
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # 2. Find User in DB
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 3. Get their Bio Profile
    bio = user.bio_profile
    if not bio:
        raise HTTPException(status_code=404, detail="Profile not initialized")

    # 4. Update the fields
    if profile_data.genotype:
        bio.genotype = profile_data.genotype
    if profile_data.blood_group:
        bio.blood_group = profile_data.blood_group
    if profile_data.rhesus_factor:
        bio.rhesus_factor = profile_data.rhesus_factor

    # 5. Save
    db.commit()
    db.refresh(bio)
    
    return {"message": "Profile updated successfully", "data": bio}

# --- 6. OCR SCANNER (THE EYES) ---
@app.post("/scan-report")
async def scan_medical_report(file: UploadFile = File(...)):
    # 1. Read the file content
    content = await file.read()
    
    # 2. Run the OCR Engine
    extraction_result = read_medical_report(content)
    
    # 3. Return results
    return {
        "filename": file.filename,
        "detected_data": extraction_result,
        "message": "Please verify this data matches your paper report."
    }
    # --- 7. VERIFY USER (GET CURRENT DATA) ---
@app.get("/users/me", response_model=UserResponse)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 1. Decode token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 2. Fetch User
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user