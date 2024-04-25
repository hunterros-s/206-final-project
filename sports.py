import requests
import time
from bs4 import BeautifulSoup
import sys

headers = {
    ':authority': 'www.pro-football-reference.com',
    ':method': 'GET',
    ':scheme': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Cookie': 'usprivacy=1Y--; srcssfull=yes; is_live=true; __cf_bm=IzxsVMas6wYmOaE2VtedWGkbOgkeUpXSL7FOKzP5VHc-1713899555-1.0.1.1-Gca8d6zJWEsIig9QBjcUX6fQlpgPY_BP_FOoP_ub4hxxbNYY8N0tPJK7QpxzHb0kd_bhGUTcheBBD5_ovvD_tA; sr_n=2%7CTue%2C%2023%20Apr%202024%2019%3A18%3A56%20GMT; sr_note_box_countdown=39',
    'Pragma': 'no-cache',
    'Priority': 'u=0, i',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

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

    game_summaries = soup.find_all('div', class_='game_summary')
    for game in game_summaries:
        loser_tag = game.find('tr', class_="loser")
        loser_text = loser_tag.find('a').get_text()
        loser_score = loser_tag.find('td', class_='right').get_text()

        winner_tag = game.find('tr', class_="winner")
        winner_text = winner_tag.find('a').get_text()
        winner_score = winner_tag.find('td', class_='right').get_text()

        td_tag = game.find('td', class_='right gamelink')
        anchor_tag = td_tag.find('a')
        if not anchor_tag:
            print('anchor tag not found?')
            continue
        href_link = anchor_tag.get('href')
        full_url = f'https://www.pro-football-reference.com{href_link}'

        data.append(
            (winner_text, winner_score, loser_text, loser_score, full_url)
        )

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
    start_time_strong_tag = soup.find('strong', string="Start Time")
    start_time_text = start_time_strong_tag.next_sibling.strip('" ')[2:]

    #stadium link
    stadium_name = soup.find('strong', string='Stadium')
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
        
        data.append(
            (winner_text, winner_score, loser_text, loser_score, date_text, time_text, address)
        )
    
    return data


