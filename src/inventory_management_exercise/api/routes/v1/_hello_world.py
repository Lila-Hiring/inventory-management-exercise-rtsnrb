"""Example module with endpoint definition."""

from fastapi import APIRouter

# Router for routes defined in this file.
hello_router = APIRouter()


@hello_router.get("/")
def hello() -> dict[str, str]:
    """Root route in the /v1 prefix."""
    return {"message": "Welcome to inventory_management_exercise!"}
