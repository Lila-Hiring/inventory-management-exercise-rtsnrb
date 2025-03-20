"""Utility functions for route handlers."""

from fastapi import HTTPException
from sqlmodel import select


def get_or_404(model, obj_id, session):
    """Get an object by ID or raise 404."""
    obj = session.get(model, obj_id)
    if not obj or obj.soft_deleted:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return obj


def list_not_soft_deleted(model, session):
    """List all non-soft-deleted objects of a model."""
    statement = select(model).where(not model.soft_deleted)
    return session.exec(statement).all()
