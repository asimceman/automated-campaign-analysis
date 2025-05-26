from typing import AsyncGenerator
from app.repositories.campaign_repository import CampaignRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import SessionLocal
from app.repositories.ad_repository import AdRepository

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        else:
            await session.commit()

def get_ad_repository(db: AsyncSession = Depends(get_db_session)) -> AdRepository:
    return AdRepository(db)

def get_campaign_repository(db: AsyncSession = Depends(get_db_session)) -> CampaignRepository:
    return CampaignRepository(db)