import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

def get_news():
    url = "https://www.investing.com/economic-calendar/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        news_list = []

        # Each row in the economic calendar table
        rows = soup.select("tr.js-event-item")
        for row in rows:
            # Skip hidden rows or missing data
            if not row.get("data-event-datetime"):
                continue

            # Time
            ts_str = row["data-event-datetime"]  # e.g. "2026-02-02 13:30:00"
            dt_obj = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
            utc_time = (dt_obj - timedelta(hours=0)).strftime("%Y-%m-%dT%H:%M:%SZ")  # adjust if needed

            # Name
            name_tag = row.select_one(".event .left .link")
            name = name_tag.text.strip() if name_tag else ""

            # Currency
            currency_tag = row.select_one(".flag")
            currency = currency_tag.get("title", "---") if currency_tag else "---"

            # Impact
            impact_tag = row.select_one(".sentiment")
            impact_map = {"low": 1, "medium": 2, "high": 3}
            impact_text = impact_tag.get("title", "low").lower() if impact_tag else "low"
            impact_level = impact_map.get(impact_text, 1)

            # Actual / Forecast / Previous
            actual_tag = row.select_one(".act")
            forecast_tag = row.select_one(".fore")
            previous_tag = row.select_one(".prev")

            news_list.append({
                "time": utc_time,
                "name": name,
                "currency": currency,
                "impact": impact_level,
                "actual": actual_tag.text.strip() if actual_tag else "",
                "forecast": forecast_tag.text.strip() if forecast_tag else "",
                "previous": previous_tag.text.strip() if previous_tag else ""
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
