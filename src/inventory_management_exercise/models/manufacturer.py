from sqlmodel import Field, Relationship, SQLModel


class Manufacturer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str  # e.g., "Dell", "HP", "Lenovo"
    city: str
    country: str
    website: str
    phone: str
    email: str

    computers: list["Computer"] = Relationship(back_populates="manufacturer")  # noqa: F821  # pyright: ignore[reportUndefinedVariable]
