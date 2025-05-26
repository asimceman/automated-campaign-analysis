import json
from pathlib import Path
from typing import List, Dict, Any
from app.schemas.analysis import AnalysisRulebook
from app.repositories.ad_repository import AdRepository

THRESHOLDS_PATH = Path(__file__).parent / "campaign_thresholds.json"

def load_thresholds() -> AnalysisRulebook:
    data = json.loads(Path(THRESHOLDS_PATH).read_text())
    return AnalysisRulebook.model_validate(data)

async def analyze_campaign_ads(ad_repository: AdRepository) -> List[Dict[str, Any]]:
    thresholds = load_thresholds()

    ads = await ad_repository.get_ads_for_campaign(campaign_id=1)

    results = []

    for ad in ads:
        violations = []

        for field, condition in thresholds.root.items():
            actual = getattr(ad, field, None)
            if actual is None:
                continue

            if condition.lt is not None and actual < condition.lt:
                violations.append(f"{field} should not be less than {float(condition.lt):.2f}, but it's {float(actual):.2f}")
            elif condition.gt is not None and actual > condition.gt:
                violations.append(f"{field} should not be greater than {float(condition.gt):.2f}, but it's {float(actual):.2f}")

            results.append({
                "ad_id": ad.id,
                "violations": violations,
            })

        if violations:
            ad.has_violations=True
        
        if not violations and ad.has_violations is True:
            ad.has_violations=None

    return results