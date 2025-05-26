from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign


class CampaignRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_campaign_by_id(self, id: int) -> Optional[Campaign]:
        result = await self.session.execute(
            select(Campaign).where(Campaign.id == id)
        )
        return result.scalar_one_or_none()
