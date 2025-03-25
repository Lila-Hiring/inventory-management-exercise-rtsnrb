from datetime import date
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class OperatingSystem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str  # e.g., "Windows 10", "Ubuntu 20.04"
    version: str  # e.g., "10.0.19045", "20.04.5"
    os_type: str  # e.g., "Windows", "Linux", "macOS"
    release_date: date | None = None

    architecture_id: int | None = Field(default=None, foreign_key="architecture.id")
    architecture: Optional["Architecture"] = Relationship(back_populates="operating_systems")  # noqa: F821  # pyright: ignore[reportUndefinedVariable]

    computers: list["Computer"] = Relationship(back_populates="operating_system")  # noqa: F821  # pyright: ignore[reportUndefinedVariable]
