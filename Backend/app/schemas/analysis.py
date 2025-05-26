from pydantic import BaseModel, RootModel
from typing import Dict, Optional

class FieldCondition(BaseModel):
    lt: Optional[float] = None
    gt: Optional[float] = None

class AnalysisRulebook(RootModel[Dict[str, FieldCondition]]):
    pass