import requests
from bs4 import BeautifulSoup
import json

def get_news():
    # We add a specific date to the URL to make sure we always see news
    url = "https://www.forexfactory.com/calendar?day=today"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        news_list = []
        
        # Look for the calendar rows
        rows = soup.select("tr.calendar__row")
        
        for row in rows:
            # Skip rows that aren't actual news (like ads or blank space)
            event_tag = row.select_one(".calendar__event")
            if not event_tag:
                continue
                
            news_item = {
                "time": row.select_one(".calendar__time").text.strip() if row.select_one(".calendar__time") else "---",
                "name": event_tag.text.strip(),
                "currency": row.select_one(".calendar__currency").text.strip() if row.select_one(".calendar__currency") else "---",
                "actual": row.select_one(".calendar__actual").text.strip() if row.select_one(".calendar__actual") else "",
                "forecast": row.select_one(".calendar__forecast").text.strip() if row.select_one(".calendar__forecast") else "",
                "previous": row.select_one(".calendar__previous").text.strip() if row.select_one(".calendar__previous") else "",
            }
            news_list.append(news_item)

        # If it's still empty (like on a weekend), add a "Weekend Mode" message
        if not news_list:
            news_list.append({
                "time": "Weekend",
                "name": "No news scheduled for today",
                "currency": "N/A",
                "actual": "", "forecast": "", "previous": ""
            })

        with open("data.json", "w") as f:
            json.dump(news_list, f, indent=4)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_news()
