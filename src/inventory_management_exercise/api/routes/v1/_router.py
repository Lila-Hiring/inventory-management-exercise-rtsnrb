from fastapi import APIRouter
from scalar_fastapi import get_scalar_api_reference

from inventory_management_exercise.api.routes.v1._hello_world import hello_router

# Router for all routes we want to expose under the `/v1` API path.
v1_router = APIRouter(prefix="/v1")
v1_router.include_router(hello_router)


@v1_router.get("/docs", include_in_schema=False)
def scalar_html():
    return get_scalar_api_reference(
        openapi_url="/v1/openapi.json",
        title="inventory_management_exercise",
    )
