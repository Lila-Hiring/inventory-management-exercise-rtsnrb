from fastapi import APIRouter
from sqlmodel import Session

from inventory_management_exercise.db import engine
from inventory_management_exercise.models.architecture import Architecture

from ._utils import get_or_404, list_not_soft_deleted

router = APIRouter()


@router.get("/architectures", response_model=list[Architecture])
def list_architectures():
    with Session(engine) as session:
        return list_not_soft_deleted(Architecture, session)


@router.get("/architectures/{architecture_id}", response_model=Architecture)
def get_architecture(architecture_id: int):
    with Session(engine) as session:
        return get_or_404(Architecture, architecture_id, session)


@router.post("/architectures", response_model=Architecture)
def create_architecture(architecture: Architecture):
    with Session(engine) as session:
        session.add(architecture)
        session.commit()
        session.refresh(architecture)
        return architecture


@router.put("/architectures/{architecture_id}", response_model=Architecture)
def update_architecture(architecture_id: int, updated_data: Architecture):
    with Session(engine) as session:
        db_arch = get_or_404(Architecture, architecture_id, session)
        for field, value in updated_data.dict(exclude_unset=True).items():
            setattr(db_arch, field, value)
        session.add(db_arch)
        session.commit()
        session.refresh(db_arch)
        return db_arch


@router.delete("/architectures/{architecture_id}")
def soft_delete_architecture(architecture_id: int):
    with Session(engine) as session:
        db_arch = get_or_404(Architecture, architecture_id, session)
        db_arch.soft_deleted = True
        session.add(db_arch)
        session.commit()
        return {"detail": "Architecture soft-deleted"}
