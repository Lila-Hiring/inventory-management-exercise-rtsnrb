from fastapi import APIRouter
from sqlmodel import Session

from inventory_management_exercise.db import engine
from inventory_management_exercise.models.manufacturer import Manufacturer

from ._utils import get_or_404, list_not_soft_deleted

router = APIRouter()


@router.get("/manufacturers", response_model=list[Manufacturer])
def list_manufacturers():
    with Session(engine) as session:
        return list_not_soft_deleted(Manufacturer, session)


@router.get("/manufacturers/{manufacturer_id}", response_model=Manufacturer)
def get_manufacturer(manufacturer_id: int):
    with Session(engine) as session:
        return get_or_404(Manufacturer, manufacturer_id, session)


@router.post("/manufacturers", response_model=Manufacturer)
def create_manufacturer(manufacturer: Manufacturer):
    with Session(engine) as session:
        session.add(manufacturer)
        session.commit()
        session.refresh(manufacturer)
        return manufacturer


@router.put("/manufacturers/{manufacturer_id}", response_model=Manufacturer)
def update_manufacturer(manufacturer_id: int, updated_data: Manufacturer):
    with Session(engine) as session:
        db_manufacturer = get_or_404(Manufacturer, manufacturer_id, session)
        for field, value in updated_data.dict(exclude_unset=True).items():
            setattr(db_manufacturer, field, value)
        session.add(db_manufacturer)
        session.commit()
        session.refresh(db_manufacturer)
        return db_manufacturer


@router.delete("/manufacturers/{manufacturer_id}")
def soft_delete_manufacturer(manufacturer_id: int):
    with Session(engine) as session:
        db_manufacturer = get_or_404(Manufacturer, manufacturer_id, session)
        db_manufacturer.soft_deleted = True
        session.add(db_manufacturer)
        session.commit()
        return {"detail": "Manufacturer soft-deleted"}
