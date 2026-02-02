import requests
import json
from datetime import datetime

def get_news():
    url = "https://cdn-nfs.forexfactory.net/ff_calendar_thisweek.json?v=123"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check the structure
        events = data.get("calendar", {}).get("events", []) or data.get("events", [])
        if not events:
            print("No events found in JSON response.")
            return

        news_list = []

        for event in events:
            if not event.get("currency") or not event.get("time"):
                continue

            # Convert timestamp (some events use 'timestamp', others 'time')
            ts = event.get("timestamp") or event.get("time")
            dt_obj = datetime.utcfromtimestamp(ts)
            utc_time = dt_obj.strftime("%Y-%m-%dT%H:%M:%SZ")

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

    except requests.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_news()
