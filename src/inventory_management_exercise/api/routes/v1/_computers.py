from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from inventory_management_exercise.db import engine
from inventory_management_exercise.models.computer import Computer

router = APIRouter()


@router.get("/computers", response_model=list[Computer])
def list_computers():
    with Session(engine) as session:
        statement = select(Computer).where(not Computer.soft_deleted)
        return session.exec(statement).all()


@router.get("/computers/{computer_id}", response_model=Computer)
def get_computer(computer_id: int):
    with Session(engine) as session:
        computer = session.get(Computer, computer_id)
        if not computer or computer.soft_deleted:
            raise HTTPException(status_code=404, detail="Computer not found")
        return computer


@router.post("/computers", response_model=Computer)
def create_computer(computer: Computer):
    with Session(engine) as session:
        session.add(computer)
        session.commit()
        session.refresh(computer)
        return computer


@router.put("/computers/{computer_id}", response_model=Computer)
def update_computer(computer_id: int, updated_data: Computer):
    with Session(engine) as session:
        computer = session.get(Computer, computer_id)
        if not computer or computer.soft_deleted:
            raise HTTPException(status_code=404, detail="Computer not found")

        for field, value in updated_data.dict(exclude_unset=True).items():
            setattr(computer, field, value)

        session.add(computer)
        session.commit()
        session.refresh(computer)
        return computer


@router.delete("/computers/{computer_id}")
def soft_delete_computer(computer_id: int):
    with Session(engine) as session:
        computer = session.get(Computer, computer_id)
        if not computer or computer.soft_deleted:
            raise HTTPException(status_code=404, detail="Computer not found")

        computer.soft_deleted = True
        session.add(computer)
        session.commit()
        return {"detail": "Computer soft-deleted"}
