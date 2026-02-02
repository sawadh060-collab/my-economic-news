import requests
import json
from datetime import datetime

def get_news():
    url = "https://cdn-nfs.forexfactory.net/ff_calendar_thisweek.json?v=123"  # FF JSON endpoint
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()  # This contains all the events

        news_list = []

        for event in data.get("events", []):
            # Skip if no currency or time
            if not event.get("currency") or not event.get("time"):
                continue

            # Convert timestamp to UTC ISO format
            dt_obj = datetime.utcfromtimestamp(event["timestamp"])
            utc_time = dt_obj.strftime("%Y-%m-%dT%H:%M:%SZ")

            # Map impact
            impact_map = {"low": 1, "medium": 2, "high": 3}
            impact_level = impact_map.get(event.get("impact", "low").lower(), 1)

            news_list.append({
                "time": utc_time,
                "name": event.get("title", ""),
                "currency": event.get("currency", "---"),
                "impact": impact_level,
                "actual": event.get("actual", ""),
                "forecast": event.get("forecast", ""),
                "previous": event.get("previous", "")
            })

        with open("data.json", "w") as f:
            json.dump(news_list, f, indent=4)

        print(f"Successfully scraped {len(news_list)} events.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_news()
