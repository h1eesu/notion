import requests
import datetime
import os

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

headers = {
    "Authorization" : f"Bearver {NOTION_API_KEY}",
    "Content-Type" : "application/json",
    "Notion-version" : "2022-06-28"
}

def create_weekly_task(title, date):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Subject": {
                "title": [{"text": {"content": title}}]
            },
            "Date": {
                "date": {"start": date}
            }
        }
    }
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        print("✅ Task created:", title, date)
    else:
        print("❌ Error:", res.text)

if __name__ == "__main__":
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)
    create_weekly_task("Weekly Task Auto", str(next_week))
