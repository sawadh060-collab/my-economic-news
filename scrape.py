import requests
from bs4 import BeautifulSoup
import json

def get_news():
    url = "https://www.forexfactory.com/calendar"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    news_list = []
    
    # Target the main calendar table rows
    rows = soup.select("tr.calendar__row")
    
    for row in rows:
        try:
            # We only want rows that actually have an event name
            event = row.select_one(".calendar__event").text.strip()
            if not event: continue

            news_list.append({
                "time": row.select_one(".calendar__time").text.strip(),
                "name": event,
                "currency": row.select_one(".calendar__currency").text.strip(),
                "actual": row.select_one(".calendar__actual").text.strip(),
                "forecast": row.select_one(".calendar__forecast").text.strip(),
                "previous": row.select_one(".calendar__previous").text.strip(),
                "impact": row.select_one(".calendar__impact span").get("title", "Low").split()[0]
            })
        except:
            continue # Skip rows that are empty or ads

    # Save to your data.json
    with open("data.json", "w") as f:
        json.dump(news_list[:15], f, indent=4) # Keep top 15 news items

if __name__ == "__main__":
    get_news()
