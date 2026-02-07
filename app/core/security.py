from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# We use Bcrypt, a hashing algorithm that is slow by design to stop hackers.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if the typed password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Turns 'secretpassword' into '$2b$12$Gb...'"""
    return pwd_context.hash(password)
    # 1. Configuration (In production, these come from environment variables)
SECRET_KEY = "my_super_secret_key_change_this_in_prod" # Crucial: Keeps tokens safe
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 2. Token Generator
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt