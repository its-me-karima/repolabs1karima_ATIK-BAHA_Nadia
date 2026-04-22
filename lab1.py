import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "Host": "github.com",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Referer": "https://github.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9"
}

data = []
for x in range (1,101):
    url = f"https://github.com/search?q=mental+health+ai&type=repositories&p={x}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    repos = soup.find_all("div", class_="Result-module__Result__Up5vk")
    for repo in repos:
        
        # title
        title_tag = repo.find("a", href=True)
        if title_tag:
            title = title_tag.text.strip()
            link = "https://github.com" + title_tag["href"]
        else:
            title = None
            link = None
    
        # description
        desc_tag = repo.find("span",class_="search-match SearchMatchText-module__searchMatchText__n6aQc prc-Text-Text-9mHv3")
        description = desc_tag.text.strip() if desc_tag else None
    
        # stars
        star_tag = repo.find("a", href=lambda x: x and "stargazers" in x)
        stars = star_tag.text.strip() if star_tag else None
    
        time_tag= repo.find("div", class_="prc-Truncate-Truncate-2G1eo")
        last_updated = time_tag.text.strip() if time_tag else None
    
        data.append([title, link, description, stars, last_updated])


df = pd.DataFrame(
    data,
    columns=["Title", "URL", "Description", "Stars", "Last Updated"]
)

df.to_csv("github_repositories.csv", index=False, encoding="utf-8")
print("CSV file created successfully")
