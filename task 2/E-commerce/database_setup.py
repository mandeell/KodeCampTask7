from sqlalchemy import create_engine

# Database URL - SQLite database file
DATABASE_URL = "sqlite:///./e-commerce.db"

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
