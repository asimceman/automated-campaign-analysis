from pydantic import BaseModel
from typing import Optional

class Campaign(BaseModel):
    id: int
    name: str
    insights: Optional[str]
    recommendations: Optional[str]

    class Config:
        orm_mode = True