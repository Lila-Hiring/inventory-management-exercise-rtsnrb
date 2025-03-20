from fastapi import APIRouter
from sqlmodel import Session

from inventory_management_exercise.db import engine
from inventory_management_exercise.models.cpu import CPU

from ._utils import get_or_404, list_not_soft_deleted

router = APIRouter()


@router.get("/cpus", response_model=list[CPU])
def list_cpus():
    with Session(engine) as session:
        return list_not_soft_deleted(CPU, session)


@router.get("/cpus/{cpu_id}", response_model=CPU)
def get_cpu(cpu_id: int):
    with Session(engine) as session:
        return get_or_404(CPU, cpu_id, session)


@router.post("/cpus", response_model=CPU)
def create_cpu(cpu: CPU):
    with Session(engine) as session:
        session.add(cpu)
        session.commit()
        session.refresh(cpu)
        return cpu


@router.put("/cpus/{cpu_id}", response_model=CPU)
def update_cpu(cpu_id: int, updated_data: CPU):
    with Session(engine) as session:
        db_cpu = get_or_404(CPU, cpu_id, session)
        for field, value in updated_data.dict(exclude_unset=True).items():
            setattr(db_cpu, field, value)
        session.add(db_cpu)
        session.commit()
        session.refresh(db_cpu)
        return db_cpu


@router.delete("/cpus/{cpu_id}")
def soft_delete_cpu(cpu_id: int):
    with Session(engine) as session:
        db_cpu = get_or_404(CPU, cpu_id, session)
        db_cpu.soft_deleted = True
        session.add(db_cpu)
        session.commit()
        return {"detail": "CPU soft-deleted"}
