from typing import List
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ad import Ad
from app.schemas.ad import AdChannelSummary

class AdRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self) -> List[Ad]:
        result = await self.session.execute(
            select(Ad).order_by(Ad.id)
        )
        return result.scalars().all()

    async def get_ads_for_campaign(self, campaign_id: int) -> List[Ad]:
        result = await self.session.execute(
            select(Ad).where(Ad.campaign_id == campaign_id).order_by(Ad.id)
        )
        return result.scalars().all()
    
    async def get_channel_summaries_by_campaign(
        self, campaign_id: int
    ) -> List[AdChannelSummary]:
        result = await self.session.execute(
            select(
                Ad.channel_used.label("channel"),
                func.avg(Ad.conversion_rate).label("average_conversion_rate"),
                func.avg(Ad.engagement_score).label("average_engagement_score"),
            )
            .where(Ad.campaign_id == campaign_id)
            .group_by(Ad.channel_used)
        )
        rows = result.all()
        return [
            AdChannelSummary(
                channel=row.channel,
                average_conversion_rate=float(row.average_conversion_rate) * 100,
                average_engagement_score=float(row.average_engagement_score),
            )
            for row in rows
        ]
