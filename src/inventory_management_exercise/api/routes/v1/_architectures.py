from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from inventory_management_exercise.db import get_session
from inventory_management_exercise.models.architecture import Architecture

from ._utils import get_or_404, list_not_soft_deleted

router = APIRouter()

# Define the dependency type once
DbSession = Annotated[Session, Depends(get_session)]


@router.get("/architectures", response_model=list[Architecture])
def list_architectures(session: DbSession):
    x = list_not_soft_deleted(Architecture, session)
    return x


@router.get("/architectures/{architecture_id}", response_model=Architecture)
def get_architecture(architecture_id: int, session: DbSession):
    return get_or_404(Architecture, architecture_id, session)


@router.post("/architectures", response_model=Architecture)
def create_architecture(architecture: Architecture, session: DbSession):
    session.add(architecture)
    session.commit()
    session.refresh(architecture)
    return architecture


@router.put("/architectures/{architecture_id}", response_model=Architecture)
def update_architecture(architecture_id: int, updated_data: Architecture, session: DbSession):
    db_arch = get_or_404(Architecture, architecture_id, session)
    for field, value in updated_data.dict(exclude_unset=True).items():
        setattr(db_arch, field, value)
    session.add(db_arch)
    session.commit()
    session.refresh(db_arch)
    return db_arch


@router.delete("/architectures/{architecture_id}")
def soft_delete_architecture(architecture_id: int, session: DbSession):
    db_arch = get_or_404(Architecture, architecture_id, session)
    db_arch.soft_deleted = True
    session.add(db_arch)
    session.commit()
    return {"detail": "Architecture soft-deleted"}
