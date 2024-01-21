from fastapi import APIRouter

from apis.v1 import route_user
from apis.v1 import route_account

api_router = APIRouter()

api_router.include_router(route_user.router, prefix="", tags=["users"])
api_router.include_router(route_account.router, prefix="", tags=["accounts"])

"""
used to import all routes to main.py file
"""