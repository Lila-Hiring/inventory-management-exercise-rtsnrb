from sqlmodel import Field, Relationship, SQLModel


class Architecture(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str  # e.g., "x86_64", "ARM64"
    description: str
    # Example: "x86_64", "ARM64", etc.

    operating_systems: list["OperatingSystem"] = Relationship()  # noqa: F821  # pyright: ignore[reportUndefinedVariable]
