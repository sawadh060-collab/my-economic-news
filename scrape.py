import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_news():
    # Forced 'today' view
    url = "https://www.forexfactory.com/calendar?day=today"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        news_list = []
        
        # Get current year/month/day to build the timestamp
        now = datetime.now()
        current_date_str = now.strftime("%Y-%m-%d")

        for row in soup.select("tr.calendar__row"):
            event_tag = row.select_one(".calendar__event")
            if not event_tag: continue
            
            # --- 1. THE TIMEZONE FIX ---
            time_text = row.select_one(".calendar__time").text.strip() if row.select_one(".calendar__time") else ""
            utc_timestamp = ""
            
            if time_text and ":" in time_text:
                try:
                    # Forex Factory time is usually like "8:30am"
                    # We combine it with today's date
                    full_time_str = f"{current_date_str} {time_text}"
                    # Convert to a data object (Assumes FF is set to default GMT/UTC)
                    dt_obj = datetime.strptime(full_time_str, "%Y-%m-%d %I:%M%p")
                    utc_timestamp = dt_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
                except:
                    utc_timestamp = time_text # Fallback for "All Day" events

            # --- 2. IMPACT DETECTION ---
            # FF uses icon classes for impact (High=red, Medium=orange, Low=yellow)
            impact_tag = row.select_one(".calendar__impact span")
            impact_class = impact_tag.get("class", []) if impact_tag else []
            impact_level = 1 # Default Low
            if "high" in str(impact_class).lower(): impact_level = 3
            elif "medium" in str(impact_class).lower(): impact_level = 2

            # --- 3. ACTUAL STATUS (Green/Red) ---
            actual_tag = row.select_one(".calendar__actual")
            actual_status = "neutral"
            if actual_tag:
                classes = actual_tag.get("class", [])
                if "better" in classes: actual_status = "better"
                elif "worse" in classes: actual_status = "worse"

            news_list.append({
                "time": utc_timestamp, # Now in Universal Format
                "name": event_tag.text.strip(),
                "currency": row.select_one(".calendar__currency").text.strip() if row.select_one(".calendar__currency") else "---",
                "impact": impact_level,
                "actual": actual_tag.text.strip() if actual_tag else "",
                "actual_status": actual_status,
                "forecast": row.select_one(".calendar__forecast").text.strip() if row.select_one(".calendar__forecast") else "",
                "previous": row.select_one(".calendar__previous").text.strip() if row.select_one(".calendar__previous") else ""
            })

        with open("data.json", "w") as f:
            json.dump(news_list, f, indent=4)
        print(f"Successfully scraped {len(news_list)} events.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_news()
