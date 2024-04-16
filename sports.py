import requests
from bs4 import BeautifulSoup

#looking for: location, date/time, final score


#url to dashboard of all the games from a particular week

'''
year = 2022
week_num = 4

summary_page_url = f'https://www.pro-football-reference.com/years/{year}/week_{week_num}.htm'
r = requests.get(summary_page_url)

#gets list of links to box scores of every game listed on the summary page
if (r.status_code == 200):
    soup = BeautifulSoup(r.content, 'html.parser')

    td_tags = soup.findAll('td', class_='right gamelink')

    boxscore_links = []

    for tag in td_tags:
        anchor_tag = tag.find('a')
        if anchor_tag:
            href_link = anchor_tag.get('href')
            full_url = f'https://www.pro-football-reference.com{href_link}'
            boxscore_links.append(full_url)

    print(boxscore_links)

else:
    print("Failed to retrieve the webpage")
'''

#indexing through all links to individual boxscores
#end up with a list of lists, each individual list containing: away score, home score, date, start time, stadium

#big_dict = []
#for link in boxscore_links:
r = requests.get('https://www.pro-football-reference.com/boxscores/202112020nor.htm')
if (r.status_code == 200):
    #game_info = []
    soup = BeautifulSoup(r.content, 'html.parser')

    #team scores
    #NEED to only take the score text
    scores = soup.findAll('div', class_='score')

    #date
    date = soup.find('div', class_='scorebox_meta')
    date_text = date.div.text

    #start time
    #NEED to take out colon for time
    start_time_strong_tag = soup.find('strong', text="Start Time")
    start_time_text = start_time_strong_tag.next_sibling.strip('" ')

    #stadium
    #do we want the stadium name or the link to the page of the stadium which has the address

    game_info = [scores[0], scores[1], date_text, start_time_text]

    print(game_info)


else:
    print("Failed to retrieve the webpage")










'''
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

'''


