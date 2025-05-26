import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base_models import Base

class Campaign(Base):
    __tablename__ = "campaign"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.Text, nullable=False)
    insights: Mapped[str] = mapped_column(sa.Text, nullable=True)
    recommendations: Mapped[str] = mapped_column(sa.Text, nullable=True)
