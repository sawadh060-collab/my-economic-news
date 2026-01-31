import requests
from bs4 import BeautifulSoup
import json
import sys

# URL forced to GMT/UTC (Timezone ID 1) for universal compatibility
URL = "https://www.investing.com/economic-calendar/?timezone=1"

# Real browser headers to prevent "403 Forbidden" errors
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "X-Requested-With": "XMLHttpRequest"
}

def scrape_investing():
    print("Connecting to Investing.com...")
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Network Error: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Target the main calendar table
    table = soup.find('table', {'id': 'economicCalendarData'})
    if not table:
        print("Error: Could not find calendar table. Investing.com might have updated their layout.")
        sys.exit(1)

    rows = table.find_all('tr', {'class': 'js-event-item'})
    news_data = []

    for row in rows:
        try:
            # 1. Extract UTC Timestamp from data attribute
            # Format usually: 2026/01/31 15:30:00
            raw_dt = row.get('data-event-datetime')
            if not raw_dt: continue
            
            # Format for JS compatibility (YYYY-MM-DDTHH:MM:SSZ)
            utc_time = raw_dt.replace("/", "-") + "Z"

            # 2. Extract Currency and Event Name
            currency = row.find('td', {'class': 'flagCur'}).text.strip()
            event_text = row.find('td', {'class': 'event'}).text.strip()

            # 3. Extract Importance (Count Bull Icons)
            # Investing.com uses 'grayFullBullishIcon' for active levels
            sentiment_td = row.find('td', {'class': 'sentiment'})
            impact = len(sentiment_td.find_all('i', {'class': 'grayFullBullishIcon'}))

            # 4. Extract Actual/Forecast/Previous
            actual = row.find('td', {'id': lambda x: x and x.startswith('eventActual')}).text.strip()
            forecast = row.find('td', {'id': lambda x: x and x.startswith('eventForecast')}).text.strip()
            previous = row.find('td', {'id': lambda x: x and x.startswith('eventPrevious')}).text.strip()

            news_data.append({
                "time": utc_time,
                "currency": currency,
                "event": event_text,
                "impact": impact,
                "actual": actual if actual else "",
                "forecast": forecast if forecast else "",
                "previous": previous if previous else ""
            })
        except Exception as e:
            print(f"Skipping row due to error: {e}")
            continue

    # Final Save
    if news_data:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, indent=2, ensure_ascii=False)
        print(f"Success! Saved {len(news_data)} events to data.json.")
    else:
        print("No news data found.")
        sys.exit(1)

if __name__ == "__main__":
    scrape_investing()
