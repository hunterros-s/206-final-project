import requests
from bs4 import BeautifulSoup

#looking for: location, date/time, final score, 

#go to ESPN schedule, scrape the href in results column, get link to individual game
#scrape from there


#url to dashboard of all the games from a particular week

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

week_num = 5
year_num = 2013

url = 'https://www.espn.com/nfl/schedule/_/week/{week_num}/year/{year_num}}/seasontype/2'
r = requests.get(url, headers=headers)
print (r.text)
soup = BeautifulSoup(r.content, 'html.parser')

tags = soup.find_all('a', class_="AnchorLink")

boxscore_links = []
for tag in tags:
    boxscore_links.append(tag.get('href'))

print (boxscore_links)
