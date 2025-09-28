import requests
from datetime import datetime, timedelta
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

def parse_date(old_datetime_str, days = 7):
    if old_datetime_str[-6] in ['+', '-']:
        old_datetime_str = old_datetime_str[:-6]
    
    # Chuyển string thành datetime
    dt = datetime.fromisoformat(old_datetime_str)
    
    # Dời ngày (giữ nguyên giờ)
    new_dt = dt + timedelta(days=days)
    
    # Chuyển ngược về string ISO 8601 để Notion nhận
    return new_dt.isoformat()


def get_tasks():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    res = requests.post(url, headers=headers)
    return res.json()["results"]

def update_task_date(page_id, old_date_start, old_date_end):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    new_date_start = parse_date(old_date_start)
    new_date_end = parse_date(old_date_end)
    payload = {
        "properties": {
            "Date": {
                "date": {
                    "start": new_date_start,
                    "end": new_date_end
                }
            }
        }
    }
    res = requests.patch(url, headers=headers, json=payload)
    if res.status_code == 200:
        print("✅ Created:", page_id, new_date_start, "to", new_date_end)
    else:
        print("❌ Error:", res.text)

def main():
    today = datetime.now().date()
    if today.weekday() != 7:
        print("Hôm nay không phải thứ Hai. Chương trình sẽ dừng lại.")
        return
    tasks = get_tasks()
    for task in tasks:
        page_id = task["id"]
        old_date_start = task["properties"]["Date"]["date"].get("start")
        old_date_end = task["properties"]["Date"]["date"].get("end")
        update_task_date(page_id, old_date_start, old_date_end)

if __name__ == "__main__":
    main()
