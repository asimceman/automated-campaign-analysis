from typing import Optional
from pydantic import BaseModel
from datetime import date


class Ad(BaseModel):
    id: int
    target_audience: str
    channel_used: str
    conversion_rate: float
    acquisition_cost: float
    roi: float
    location: str
    language: str
    clicks: int
    impressions: int
    engagement_score: int
    ad_date: date
    has_violations: Optional[bool]

    class Config:
        from_attributes = True

class AdChannelSummary(BaseModel):
    channel: str
    average_conversion_rate: float
    average_engagement_score: float