from app.repositories.campaign_repository import CampaignRepository
from app.notifications.email_service import send_email
from fastapi import APIRouter, Depends, Query
from typing import List
from app.analyzers.campaign_analyser import analyze_campaign_ads
from app.deps import get_ad_repository, get_campaign_repository
from app.llm_clients.insight_service import generate_insights_and_recommendation_for_campaign
from app.schemas.ad import Ad, AdChannelSummary
from app.repositories.ad_repository import AdRepository

router = APIRouter(prefix="/ads", tags=["Ads"])

@router.get("/all", response_model=List[Ad])
async def get_all_ads(ad_repository: AdRepository = Depends(get_ad_repository)):
    return await ad_repository.get_all()

@router.post("/analyze-dataset")
async def analyze_dataset(ad_repository: AdRepository = Depends(get_ad_repository), campaign_repository: CampaignRepository = Depends(get_campaign_repository), campaign_id: int = Query(..., description="ID of the campaign"),):
    violations = await analyze_campaign_ads(ad_repository)

    if violations:
        campaign_name, insights, recommendations = await generate_insights_and_recommendation_for_campaign(campaign_id, ad_repository, campaign_repository)

        send_email(
            subject=f"Campaign {campaign_name} has new insights and recommendations!",
            insights=insights,
            recommendations=recommendations
        )


@router.get("/channel-summary", response_model=List[AdChannelSummary])
async def get_campaign_channel_summary(
    campaign_id: int = Query(..., description="ID of the campaign"),
    ad_repository: AdRepository = Depends(get_ad_repository),
):
    return await ad_repository.get_channel_summaries_by_campaign(campaign_id)