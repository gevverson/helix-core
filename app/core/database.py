from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# The Connection String: User:Pass@Host:Port/DB_Name
SQLALCHEMY_DATABASE_URL = "postgresql://helix_admin:biological_secrecy_key@localhost/helix_core_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
