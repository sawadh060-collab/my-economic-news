import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URL forced to GMT (Timezone ID 1) to ensure global compatibility
URL = "https://www.investing.com/economic-calendar/?timezone=1"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

def scrape_investing():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print("Failed to fetch data")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'economicCalendarData'})
    rows = table.find_all('tr', {'class': 'js-event-item'})

    news_data = []

    for row in rows:
        try:
            # 1. Extract UTC Timestamp
            # Investing.com provides a data-event-datetime attribute
            raw_time = row.get('data-event-datetime').replace('/', '-')
            utc_time = f"{raw_time}:00Z" # Adding 'Z' makes it a formal UTC string

            # 2. Extract Currency & Event
            curr = row.find('td', {'class': 'flagCur'}).text.strip()
            event = row.find('td', {'class': 'event'}).text.strip()

            # 3. Extract Impact (Bulls)
            # We count how many 'full' bull icons are in the sentiment div
            sentiment_td = row.find('td', {'class': 'sentiment'})
            bulls = len(sentiment_td.find_all('i', {'class': 'grayFullBullishIcon'}))

            # 4. Extract Numbers
            actual = row.find('td', {'id': lambda x: x and x.startswith('eventActual')}).text.strip()
            forecast = row.find('td', {'id': lambda x: x and x.startswith('eventForecast')}).text.strip()
            previous = row.find('td', {'id': lambda x: x and x.startswith('eventPrevious')}).text.strip()

            news_data.append({
                "time": utc_time,
                "currency": curr,
                "event": event,
                "impact": bulls,
                "actual": actual,
                "forecast": forecast,
                "previous": previous
            })
        except (AttributeError, TypeError):
            continue # Skip rows that aren't actual news events

    # Save to JSON for GitHub
    with open('data.json', 'w') as f:
        json.dump(news_data, f, indent=2)
    print(f"Successfully scraped {len(news_data)} events.")

if __name__ == "__main__":
    scrape_investing()
