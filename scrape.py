import requests
from bs4 import BeautifulSoup
import json

def get_news():
    url = "https://www.forexfactory.com/calendar"
    # This header makes you look more like a real human browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    news_list = []
    
    # We target the table rows specifically
    rows = soup.find_all("tr", class_="calendar__row")
    
    for row in rows:
        # Find the event name cell
        event_cell = row.find("td", class_="calendar__event")
        if event_cell:
            title = event_cell.text.strip()
            # Find the currency cell
            currency = row.find("td", class_="calendar__currency").text.strip()
            
            news_list.append({
                "title": title,
                "currency": currency,
                "impact": "Check site"
            })
            
    # If the list is STILL empty, let's add a "Test" item so your AI Studio doesn't break
    if not news_list:
        news_list.append({"title": "No news found (Market might be closed)", "currency": "N/A", "impact": "Low"})

    with open("data.json", "w") as f:
        json.dump(news_list, f, indent=4)

if __name__ == "__main__":
    get_news()
