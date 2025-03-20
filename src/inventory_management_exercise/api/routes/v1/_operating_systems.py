from fastapi import APIRouter
from sqlmodel import Session

from inventory_management_exercise.db import engine
from inventory_management_exercise.models.operating_system import OperatingSystem

from ._utils import get_or_404, list_not_soft_deleted

router = APIRouter()


@router.get("/operatingsystems", response_model=list[OperatingSystem])
def list_operating_systems():
    with Session(engine) as session:
        return list_not_soft_deleted(OperatingSystem, session)


@router.get("/operatingsystems/{os_id}", response_model=OperatingSystem)
def get_operating_system(os_id: int):
    with Session(engine) as session:
        return get_or_404(OperatingSystem, os_id, session)


@router.post("/operatingsystems", response_model=OperatingSystem)
def create_operating_system(operating_system: OperatingSystem):
    with Session(engine) as session:
        session.add(operating_system)
        session.commit()
        session.refresh(operating_system)
        return operating_system


@router.put("/operatingsystems/{os_id}", response_model=OperatingSystem)
def update_operating_system(os_id: int, updated_data: OperatingSystem):
    with Session(engine) as session:
        db_os = get_or_404(OperatingSystem, os_id, session)
        for field, value in updated_data.dict(exclude_unset=True).items():
            setattr(db_os, field, value)
        session.add(db_os)
        session.commit()
        session.refresh(db_os)
        return db_os


@router.delete("/operatingsystems/{os_id}")
def soft_delete_operating_system(os_id: int):
    with Session(engine) as session:
        db_os = get_or_404(OperatingSystem, os_id, session)
        db_os.soft_deleted = True
        session.add(db_os)
        session.commit()
        return {"detail": "OperatingSystem soft-deleted"}
