import requests
import time
from bs4 import BeautifulSoup

#looking for: location, date/time, final score


#url to dashboard of all the games from a particular week


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

    td_tags = soup.findAll('td', class_='right gamelink')

    boxscore_links = []

    for tag in td_tags:
        anchor_tag = tag.find('a')
        if anchor_tag:
            href_link = anchor_tag.get('href')
            full_url = f'https://www.pro-football-reference.com{href_link}'
            boxscore_links.append(full_url)

    return True, boxscore_links

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

def get_all_boxscores(boxscore_links):
    data = []
    for boxscore_link in boxscore_links:
        time.sleep(.2)
        success, boxscore_info = get_box_score(boxscore_link)
        if not success:
            continue

        score_a, score_b, date_text, time_text, stadium_link = boxscore_info

        time.sleep(.2)
        success, address = get_stadium_info(stadium_link)
        if not success:
            continue
        
        data.append(
            (score_a, score_b, date_text, time_text, address)
        )
    
    return data


success, links = get_game_links(2022, 4)
if not success:
    exit(1)
print(get_all_boxscores(links))



