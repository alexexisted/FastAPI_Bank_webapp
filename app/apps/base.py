from fastapi import APIRouter
from apps.v1 import route_account, route_login

app_router = APIRouter()

app_router.include_router(
    route_account.router, prefix="", tags=["Account"], include_in_schema=False
)
app_router.include_router(
    route_login.router, prefix="", tags=["Login"], include_in_schema=False
)

