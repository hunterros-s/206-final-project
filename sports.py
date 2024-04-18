import requests
import time
from bs4 import BeautifulSoup
import sys
import time

#looking for: location, date/time, final score

#url to dashboard of all the games from a particular week

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

year = 2022
week_num = 4

summary_page_url = f'https://www.pro-football-reference.com/years/{year}/week_{week_num}.htm'
r = requests.get(summary_page_url, headers=headers)

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

    #print(boxscore_links)

else:
    print(f"Failed to retrieve the webpage. Status code: {r.status_code} - {r.reason}")
    sys.exit(1)



#indexing through all links to individual boxscores
#end up with a list of lists, each individual list containing: away score, home score, date, start time, stadium address


for boxscore in boxscore_links:
    r = requests.get(boxscore, headers=headers)
    time.sleep(1)
    if (r.status_code == 200):
        #game_info = []
        soup = BeautifulSoup(r.content, 'html.parser')

        #team scores
        score_divs = soup.findAll('div', class_='score')
        scores = [div.get_text() for div in score_divs]

        #date
        date = soup.find('div', class_='scorebox_meta')
        date_text = date.div.text

        #start time
        #final slice is to take out ": " before the time
        start_time_strong_tag = soup.find('strong', string="Start Time")
        start_time_text = start_time_strong_tag.next_sibling.strip('" ')[2:]

        #stadium
        #do we want the stadium name or the link to the page of the stadium which has the address
        stadium_name = soup.find('strong', string='Stadium')
        stadium_href = stadium_name.next_sibling.next_sibling.get('href')
        stadium_link = f'https://www.pro-football-reference.com{stadium_href}'

        #using stadium link to get zip code of stadium
        r = requests.get(stadium_link, headers=headers)
        time.sleep(1)
        if (r.status_code == 200):
            soup = BeautifulSoup(r.content, 'html.parser')
            meta_div = soup.find('div', id='meta')
            address_p = meta_div.find('p')
            #zipcode = address_p.get_text()[-5:]

            #print(address_text)

        else:
            address_p = 'Failed to find'


        game_info = [scores[0], scores[1], date_text, start_time_text, address_p]

        print(game_info)

    else:
        print("Failed to retrieve the webpage")




# year = 2022
# week_num = 4

def get_game_links(year, week_num):
    summary_page_url = f'https://www.pro-football-reference.com/years/{year}/week_{week_num}.htm'

    try:
        output = requests.get(summary_page_url)
        output.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False, None

    soup = BeautifulSoup(output.content, 'html.parser')

    data = []

    game_summaries = soup.finalAll('div', class_='game_summary expanded nohover ')
    for game in game_summaries:
        loser_tag = game.find('tr', class_="loser")
        loser_text = loser_tag.find('a').get_text()
        loser_score = loser_tag.find('td', class_='right').get_text()

        winner_tag = game.find('tr', class_="winner")
        winner_text = winner_tag.find('a').get_text()
        winner_score = winner_tag.find('td', class_='right').get_text()

        td_tag = soup.find('td', class_='right gamelink')
        anchor_tag = td_tag.find('a')
        if not anchor_tag:
            print('anchor tag not found?')
            continue
        href_link = anchor_tag.get('href')
        full_url = f'https://www.pro-football-reference.com{href_link}'

        data.append(
            (winner_text, winner_score, loser_text, loser_score, full_url)
        )
        #boxscore_links.append(full_url)
        

    # td_tags = soup.findAll('td', class_='right gamelink')

    # boxscore_links = []

    # for tag in td_tags:
    #     anchor_tag = tag.find('a')
    #     if anchor_tag:
    #         href_link = anchor_tag.get('href')
    #         full_url = f'https://www.pro-football-reference.com{href_link}'
    #         boxscore_links.append(full_url)

    return True, data

def get_stadium_info(stadium_link):
    #using stadium link to get zip code of stadium
    try:
        output = requests.get(stadium_link)
        output.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False, None

    soup = BeautifulSoup(output.content, 'html.parser')
    meta_div = soup.find('div', id='meta')
    address_p = meta_div.find('p')
    address_text = address_p.get_text()

    return True, address_text


def get_box_score(boxscore_link):
    try:
        output = requests.get(boxscore_link)
        output.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False, None
    
    soup = BeautifulSoup(output.content, 'html.parser')

    #team scores
    score_divs = soup.findAll('div', class_='score')
    scores = [div.get_text() for div in score_divs]

    #team names
    #team_divs = soup.findAll('strong', class_='media-item logo loader')

    #date
    date = soup.find('div', class_='scorebox_meta')
    date_text = date.div.text

    #start time
    #final slice is to take out ": " before the time
    start_time_strong_tag = soup.find('strong', text="Start Time")
    start_time_text = start_time_strong_tag.next_sibling.strip('" ')[2:]

    #stadium
    #do we want the stadium name or the link to the page of the stadium which has the address
    stadium_name = soup.find('strong', text='Stadium')
    stadium_href = stadium_name.next_sibling.next_sibling.get('href')
    stadium_link = f'https://www.pro-football-reference.com{stadium_href}'

    return True, (scores[0], scores[1], date_text, start_time_text, stadium_link)

def get_all_boxscores(boxscore_summaries):
    data = []
    for winner_text, winner_score, loser_text, loser_score, full_url in boxscore_summaries:
        time.sleep(1)
        success, boxscore_info = get_box_score(full_url)
        if not success:
            continue

        score_a, score_b, date_text, time_text, stadium_link = boxscore_info

        time.sleep(1)
        success, address = get_stadium_info(stadium_link)
        if not success:
            continue

        print((winner_text, winner_score, loser_text, loser_score, date_text, time_text, address))
        
        data.append(
            (winner_text, winner_score, loser_text, loser_score, date_text, time_text, address)
        )
    
    return data


success, data = get_game_links(2022, 4)
#if not success:
#    exit(1)
#print(get_all_boxscores(data))



