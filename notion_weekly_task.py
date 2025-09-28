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

def query_current_week():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    sunday = monday + datetime.timedelta(days=6)
    # monday = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=7)
    # sunday = monday + datetime.timedelta(days=6)
    print("Query from:", monday, "to:", sunday)

    data = {
        "filter": {
            "and": [
                {
                    "property": "Date", "date": {"on_or_after": monday.isoformat()}
                },
                {
                    "property": "Date", "date": {"on_or_before": sunday.isoformat()}
                }
            ]
        }
    }
    res = requests.post(url, headers=headers, json=data)
    return res.json()["results"]

def create_task(title, start, end, room, dayofweek):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Subject": {"title": [{"text": {"content": title}}]},
            "Date": {
                "date": {
                    "start": start, 
                    "end": end
                }
            },
            "Day of Week": {
                "select": {"name": dayofweek}
            },
            "Room": {
                "rich_text": [{"text": {"content": room}}]
            }
        }
    }
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        print("✅ Created:", title, start)
    else:
        print("❌ Error:", res.text)

def main():
    events = query_current_week()
    for e in events:
        props = e["properties"]
        title = props["Subject"]["title"][0]["text"]["content"]
        start = props["Date"]["date"]["start"]
        end = props["Date"]["date"]["end"]
        room = props["Room"]["rich_text"][0]["text"]["content"] if props["Room"]["rich_text"] else ""
        dayofweek = props["Day of Week"]["select"]["name"]

        start_dt = datetime.datetime.fromisoformat(start.replace("Z","+00:00"))
        end_dt = datetime.datetime.fromisoformat(end.replace("Z","+00:00")) if end else None

        # cộng thêm 7 ngày
        new_start = (start_dt + datetime.timedelta(days=7)).isoformat()
        new_end = (end_dt + datetime.timedelta(days=7)).isoformat() if end_dt else None

        create_task(title, new_start, new_end, room, dayofweek)

if __name__ == "__main__":
    main()
