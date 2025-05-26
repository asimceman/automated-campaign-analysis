import asyncio
import csv
from datetime import datetime
from pathlib import Path
from app.database.session import SessionLocal
from app.models.ad import Ad
from app.models.campaign import Campaign


CSV_PATH = Path(__file__).parent / "marketing_campaign_performance_dataset.csv"

def create_campaign() -> Campaign:
    return Campaign(
        id=1,
        name="Facebook Campaign",
        insights=None,
        recommendations=None
    )

def transformed_row(row: dict) -> Ad:
    return Ad(
        id=int(row["ID"]),
        target_audience=row["Target_Audience"],
        channel_used=row["Channel_Used"],
        conversion_rate=float(row["Conversion_Rate"]),
        acquisition_cost=float(row["Acquisition_Cost"].replace("$", "").replace(",", "").strip()),
        roi=float(row["ROI"]),
        location=row["Location"],
        language=row["Language"],
        clicks=int(row["Clicks"]),
        impressions=int(row["Impressions"]),
        engagement_score=int(row["Engagement_Score"]),
        ad_date=datetime.strptime(row["Date"], "%m/%d/%Y").date(),
        has_violations=None,
        campaign_id=1
    )

async def seed() -> None:
    async with SessionLocal() as session:
        campaign = create_campaign()
        session.add(campaign)
        await session.commit()
        with open(CSV_PATH, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            ads = [transformed_row(row) for row in reader]
            session.add_all(ads)
            await session.commit()
            print(f"Seeded {len(ads)} ads.")

if __name__ == "__main__":
    asyncio.run(seed())