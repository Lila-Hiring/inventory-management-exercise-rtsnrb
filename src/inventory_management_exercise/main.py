"""inventory_management_exercise FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from inventory_management_exercise.api.routes.base import base_router
from inventory_management_exercise.api.routes.v1 import v1_router

app = FastAPI(
    title="inventory_management_exercise",
    description="A FastAPI and React programming exercise",
    version="0.1.0",
    openapi_url="/v1/openapi.json",
    # Scalar UI is hosted at /v1/docs, so we don't need Swagger, nor ReDoc.
    docs_url=None,
    redoc_url=None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(base_router)
app.include_router(v1_router)
