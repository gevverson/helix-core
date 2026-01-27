from app.core.database import engine
from app.domain import models

print("--- INITIALIZING DATABASE (POSTGRESQL) ---")
print("1. Connecting to Docker Container...")
# This line creates the tables inside your Postgres container
models.Base.metadata.create_all(bind=engine)
print("✅ 2. Tables created successfully.")
print("3. 'The Iron Gate' backend is fully operational.")
