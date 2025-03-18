"""Routes served from the `/` API path.

This is an example of a single file module that contains all the routes and the
router itself.
"""

from datetime import UTC, datetime
from importlib import metadata

from fastapi import APIRouter
from pydantic import BaseModel

base_router = APIRouter()


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    version: str
    current_time: datetime


@base_router.get("/healthz")
def health() -> HealthResponse:
    """Health check endpoint.

    Returns:
        HealthResponse: Object containing version and current time information.
    """
    version = "unknown"
    try:
        version = metadata.version("inventory_management_exercise")
    except metadata.PackageNotFoundError:
        pass

    return HealthResponse(
        version=version,
        current_time=datetime.now(UTC),
    )


__all__ = ["base_router"]
