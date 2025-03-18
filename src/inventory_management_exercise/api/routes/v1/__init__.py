"""Routes served from the `/` API path.

This package is an example of splitting the routes into separate modules."""

from inventory_management_exercise.api.routes.v1._router import v1_router

__all__ = ["v1_router"]
