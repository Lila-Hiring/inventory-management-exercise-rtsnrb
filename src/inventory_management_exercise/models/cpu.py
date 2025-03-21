from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class CPU(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    model: str  # e.g., "Core i7"
    manufacturer: str  # e.g., "Intel", "AMD"
    cores: int

    architecture_id: int | None = Field(default=None, foreign_key="architecture.id")
    architecture: Optional["Architecture"] = Relationship()  # noqa: F821  # pyright: ignore[reportUndefinedVariable]

    computers: list["Computer"] = Relationship(back_populates="cpu")  # noqa: F821  # pyright: ignore[reportUndefinedVariable]
