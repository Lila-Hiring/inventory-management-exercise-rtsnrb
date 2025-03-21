"""Script to import inventory data from CSV."""

import csv
from datetime import date, datetime
from pathlib import Path
from typing import Any

from sqlmodel import Session, select

from inventory_management_exercise.db import engine
from inventory_management_exercise.models.architecture import Architecture
from inventory_management_exercise.models.computer import Computer
from inventory_management_exercise.models.cpu import CPU
from inventory_management_exercise.models.manufacturer import Manufacturer
from inventory_management_exercise.models.operating_system import OperatingSystem


def parse_date(date_str: str) -> date | None:
    """Parse date string to datetime object."""
    if not date_str:
        return None
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def get_or_create(session: Session, model_class: type, **kwargs) -> Any:
    """Get existing record or create new one."""
    # Remove None values from kwargs
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # Try to find existing record
    statement = select(model_class)
    for key, value in kwargs.items():
        statement = statement.where(getattr(model_class, key) == value)
    existing = session.exec(statement).first()

    if existing:
        return existing

    # Create new record if not found
    new_record = model_class(**kwargs)
    session.add(new_record)
    session.commit()
    session.refresh(new_record)
    return new_record


def import_csv(file_path: str | Path) -> None:
    """Import inventory data from CSV file."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    with Session(engine) as session:
        with open(file_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Create or get architecture
                architecture = get_or_create(
                    session,
                    Architecture,
                    name=row["architecture_name"],
                    description=row["architecture_description"],
                )

                # Create or get manufacturer
                manufacturer = get_or_create(
                    session,
                    Manufacturer,
                    name=row["manufacturer_name"],
                    city=row["manufacturer_city"],
                    country=row["manufacturer_country"],
                    website=row["manufacturer_website"],
                    phone=row["manufacturer_phone"],
                    email=row["manufacturer_email"],
                )

                # Create or get CPU
                cpu = get_or_create(
                    session,
                    CPU,
                    model=row["cpu_model"],
                    manufacturer=row["cpu_manufacturer"],
                    cores=int(row["cpu_cores"]),
                    architecture_id=architecture.id,
                )

                # Create or get operating system
                operating_system = get_or_create(
                    session,
                    OperatingSystem,
                    name=row["operating_system_name"],
                    version=row["operating_system_version"],
                    os_type=row["operating_system_os_type"],
                    architecture_id=architecture.id,
                )

                # Create computer
                computer = Computer(
                    computer_type=row["computer_computer_type"],
                    purchase_date=parse_date(row["computer_purchase_date"]),
                    original_cost=float(row["computer_original_cost"]) if row["computer_original_cost"] else None,
                    installed_memory=int(row["computer_installed_memory"])
                    if row["computer_installed_memory"]
                    else None,
                    max_memory=int(row["computer_max_memory"]) if row["computer_max_memory"] else None,
                    system_model=row["computer_system_model"],
                    serial_number=row["computer_serial_number"],
                    manufacturer_id=manufacturer.id,
                    cpu_id=cpu.id,
                    operating_system_id=operating_system.id,
                )
                session.add(computer)
                session.commit()
                session.refresh(computer)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m inventory_management_exercise.scripts.import_inventory <path_to_csv>")
        sys.exit(1)

    try:
        import_csv(sys.argv[1])
        print("Import completed successfully")
    except Exception as e:
        print(f"Error during import: {e}")
        sys.exit(1)
