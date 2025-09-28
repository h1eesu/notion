import os
from dotenv import load_dotenv
import requests

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
}

res = requests.get(url, headers=headers)
print(res.status_code)
print(res.text)