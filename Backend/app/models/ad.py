import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base_models import Base
from datetime import date


class Ad(Base):
    __tablename__ = "ad"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)

    target_audience: Mapped[str] = mapped_column(sa.Text, nullable=False)
    channel_used: Mapped[str] = mapped_column(sa.Text, nullable=False)
    
    conversion_rate: Mapped[float] = mapped_column(sa.Numeric, nullable=False)
    acquisition_cost: Mapped[float] = mapped_column(sa.Numeric, nullable=False)
    roi: Mapped[float] = mapped_column(sa.Numeric, nullable=False)

    location: Mapped[str] = mapped_column(sa.Text, nullable=False)
    language: Mapped[str] = mapped_column(sa.Text, nullable=False)
    clicks: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    impressions: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    engagement_score: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    ad_date: Mapped[date] = mapped_column(sa.Date, nullable=False)

    has_violations: Mapped[bool] = mapped_column(sa.Boolean, nullable=True)

    campaign_id: Mapped[int] = mapped_column(sa.ForeignKey("campaign.id"), nullable=True)