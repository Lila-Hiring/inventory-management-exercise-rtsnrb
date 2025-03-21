from datetime import date
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from .cpu import CPU
from .manufacturer import Manufacturer
from .operating_system import OperatingSystem


class Computer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    computer_type: str  # e.g., "Laptop", "Desktop", "Rack Server", "IoT", ...
    purchase_date: date | None = None
    original_cost: float | None = None
    installed_memory: int | None = None
    max_memory: int | None = None
    system_model: str | None = None
    serial_number: str | None = None
    soft_deleted: bool = Field(default=False)

    manufacturer_id: int | None = Field(default=None, foreign_key="manufacturer.id")
    operating_system_id: int | None = Field(default=None, foreign_key="operatingsystem.id")
    cpu_id: int | None = Field(default=None, foreign_key="cpu.id")
    cpu_count: int | None = Field(default=1)

    manufacturer: Optional["Manufacturer"] = Relationship(back_populates="computers")  # noqa: F821
    operating_system: Optional["OperatingSystem"] = Relationship(back_populates="computers")  # noqa: F821
    cpu: Optional["CPU"] = Relationship(back_populates="computers")  # noqa: F821
