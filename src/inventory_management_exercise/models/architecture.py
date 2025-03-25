from sqlmodel import Field, Relationship, SQLModel

from .operating_system import OperatingSystem


class Architecture(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    soft_deleted: bool = Field(default=False)
    operating_systems: list["OperatingSystem"] = Relationship(back_populates="architecture")
