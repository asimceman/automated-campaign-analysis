from fastapi import APIRouter

from app.api import ad
from app.api import campaign

api_router = APIRouter()
api_router.include_router(ad.router)
api_router.include_router(campaign.router)