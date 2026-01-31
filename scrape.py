import requests
from bs4 import BeautifulSoup
import json

def get_news():
    url = "https://www.forexfactory.com/calendar?day=today"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        news_list = []
        
        for row in soup.select("tr.calendar__row"):
            event_tag = row.select_one(".calendar__event")
            if not event_tag: continue
            
            # Detect Actual color/status
            actual_tag = row.select_one(".calendar__actual")
            actual_status = "neutral"
            if actual_tag:
                # Forex Factory uses these classes for green/red numbers
                if "better" in actual_tag.get("class", []): actual_status = "better"
                elif "worse" in actual_tag.get("class", []): actual_status = "worse"

            news_list.append({
                "time": row.select_one(".calendar__time").text.strip() if row.select_one(".calendar__time") else "---",
                "name": event_tag.text.strip(),
                "currency": row.select_one(".calendar__currency").text.strip() if row.select_one(".calendar__currency") else "---",
                "actual": actual_tag.text.strip() if actual_tag else "",
                "actual_status": actual_status, # NEW: This tells the widget if it's Green or Red
                "forecast": row.select_one(".calendar__forecast").text.strip() if row.select_one(".calendar__forecast") else "",
                "previous": row.select_one(".calendar__previous").text.strip() if row.select_one(".calendar__previous") else "",
            })

        with open("data.json", "w") as f:
            json.dump(news_list, f, indent=4)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_news()
