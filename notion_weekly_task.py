import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")

headers = {
    "Authorization" : f"Bearer {NOTION_API_KEY}",
    "Content-Type" : "application/json",
    "Notion-version" : "2022-06-28"
}

def create_weekly_task(title, start_date, end_date):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Subject": {
                "title": [{"text": {"content": title}}]
            },
            "Start Date": {
                "date": {"start": start_date}
            },
            "End Date": {
                "date": {"start": end_date}
            }
        }
    }
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        print("✅ Task created:", title, start_date, end_date)
    else:
        print("❌ Error:", res.text)

if __name__ == "__main__":
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)
    create_weekly_task("Weekly Task Auto", str(next_week), str(next_week))
