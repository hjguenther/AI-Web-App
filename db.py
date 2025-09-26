from sqlalchemy import create_engine
import os

# Render will inject this securely
db_url = os.getenv("DATABASE_URL")

# Connect with SSL required (Render uses SSL by default)
engine = create_engine(db_url, connect_args={"sslmode": "require"})
