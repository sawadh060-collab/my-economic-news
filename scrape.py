import requests
from bs4 import BeautifulSoup
import json

# This tells the website we are a normal person browsing
headers = {"User-Agent": "Mozilla/5.0"}

def get_news():
    url = "https://www.forexfactory.com/calendar"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    news_list = []
    
    # We look for the news rows on the page
    rows = soup.select(".calendar__row")
    for row in rows[:10]: # Just get the first 10 news items
        event = row.select_one(".calendar__event")
        if event:
            news_list.append({
                "title": event.text.strip(),
                "impact": "Check site" 
            })
            
    # This saves the news into our data.json file
    with open("data.json", "w") as f:
        json.dump(news_list, f)

get_news()
