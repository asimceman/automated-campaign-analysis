import os
import requests
from app.settings import settings

MAILGUN_API_KEY = settings.MAILGUN_API_KEY
MAILGUN_DOMAIN = settings.MAILGUN_DOMAIN
FROM_EMAIL = f"Alerts <postmaster@{MAILGUN_DOMAIN}>"
TO_EMAIL = settings.RECIPIENT_EMAIL
DASHBOARD_URL = os.environ.get("DASHBOARD_URL", "http://localhost:5173")

def send_email(subject: str, insights: str, recommendations: str):
    html = (
        "Insights and recommendations are:"
        "<br>"
        f"<p>{insights}</p>"
        f"<p>For more details check out <a href='{DASHBOARD_URL}'>our dashboard</a>!</p>"
        f"<p>{recommendations}</p>"
    )

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": FROM_EMAIL,
            "to": TO_EMAIL,
            "subject": subject,
            "html": html,
        }
    )

    if response.status_code != 200:
        print("❌ Failed to send alert:", response.text)
    else:
        print("✅ Alert sent:", subject)