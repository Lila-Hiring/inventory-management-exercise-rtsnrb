"""Database configuration."""

from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

# Get the absolute path to the database file
DB_PATH = Path(__file__).parent.parent / "inventory.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)


def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    breakpoint()
    with Session(engine) as session:
        yield session


# Make sure to export the function
__all__ = ["engine", "get_session"]
