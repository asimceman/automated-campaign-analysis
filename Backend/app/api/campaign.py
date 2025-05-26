from app.repositories.campaign_repository import CampaignRepository
from app.schemas.campaign import Campaign
from fastapi import APIRouter, Depends, Query
from app.deps import get_campaign_repository

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

@router.get("", response_model=Campaign)
async def read_campaign(
    id: int = Query(..., description="ID of the campaign"),
    campaign_repository: CampaignRepository = Depends(get_campaign_repository),
):
    return await campaign_repository.get_campaign_by_id(id)
