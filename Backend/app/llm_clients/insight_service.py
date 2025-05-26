from typing import List
from app.settings import settings
from openai import OpenAI
from app.models.ad import Ad
from app.repositories.ad_repository import AdRepository
from app.repositories.campaign_repository import CampaignRepository



client = OpenAI(
    base_url=settings.OPEN_AI_URL,
    api_key=settings.OPENAI_API_KEY,
)

def build_campaign_prompt(ads: List[Ad]) -> str:
    prompt = "Analyze the following dataset of campaigns. Your task is to:\n"
    prompt += (
        "- Identify anomalies (e.g., unusual metrics like very high acquisition cost, very low ROI)\n"
        "- Calculate basic metrics if useful (averages, comparisons)\n"
        "- Summarize key insights (5/6 sentences)\n"
        "- Provide actionable recommendations (5/6 sentences)\n\n"
    )

    prompt += "CAMPAIGN DATA:\n"

    for i, ad in enumerate(ads, start=1):
        prompt += (
            f"\ad {i}:\n"
            f"- Location: {ad.location}\n"
            f"- Language: {ad.language}\n"
            f"- Audience: {ad.target_audience}\n"
            f"- Conversion Rate: {float(ad.conversion_rate):.2f}\n"
            f"- ROI: {float(ad.roi):.2f}\n"
            f"- Engagement Score: {float(ad.engagement_score):.2f}\n"
            f"- Acquisition Cost: {float(ad.acquisition_cost):.2f}\n"
            f"- Clicks: {ad.clicks}, Impressions: {ad.impressions}\n"
            f"- Date: {ad.ad_date}\n"
        )

    return prompt


async def generate_insight(prompt: str, model: str = "mistralai/devstral-small:free") -> str:
    response = client.chat.completions.create(
        max_tokens=13000,
        model=model,
        messages=[
                {
            "role": "system",
            "content": (
                "You are a senior marketing analyst. "
                "You must perform the full analysis of the marketing campaign. "
                "You need to be able to help analysts to find where the campaign should be adjusted to get better results. "
                "Your role is to spot the trends and when something is off in the data, you need to be able to give concrete recommendations on how to fix it. "
                "You have to keep your response and completion under 13 000 tokens! "
                "Your response MUST consist of two lines and only two lines. Those lines should have 5/6 sentances. However much you can squeeze in the limit while still being clear and helpful. 1st line is the 'Insights: ' and 2nd line is the 'Recommendations:'. Don't have an empty line in between of them. "
            )
        },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print('result: ', response.choices[0].message.content)
    return response.choices[0].message.content

async def generate_insights_and_recommendation_for_campaign(campaign_id: int, ad_repository: AdRepository, campaign_repository: CampaignRepository
) -> tuple[str, str]:
    ads = await ad_repository.get_ads_for_campaign(campaign_id)
    prompt = build_campaign_prompt(ads)

    recommendation_text = await generate_insight(prompt)
    
    # Step 1: Remove asterisks
    recommendation_text = recommendation_text.replace("*", "")

    # Step 2: Strip and remove all empty lines
    lines = [line.strip() for line in recommendation_text.split("\n") if line.strip()]

    # Step 3: Rejoin cleaned lines
    cleaned_text = "\n".join(lines)

    # Step 4: Extract insights and recommendations
    insights = ""
    recommendations = ""

    if "Insights:" in cleaned_text and "Recommendations:" in cleaned_text:
        insights_part, recommendations_part = cleaned_text.split("Recommendations:", 1)
        insights = insights_part.replace("Insights:", "").strip()
        recommendations = recommendations_part.strip()
    else:
        # Fallback if "Recommendations:" is missing
        insights = cleaned_text.strip()

    # Now `insights` and `recommendations` are both clean strings

    campaign = await campaign_repository.get_campaign_by_id(1)

    campaign.insights = insights
    campaign.recommendations = recommendations

    campaign_name = campaign.name

    return campaign_name, insights, recommendations
