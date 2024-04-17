import requests
from bs4 import BeautifulSoup

#looking for: location, date/time, final score


#url to dashboard of all the games from a particular week


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

    #print(boxscore_links)

else:
    print("Failed to retrieve the webpage")


#indexing through all links to individual boxscores
#end up with a list of lists, each individual list containing: away score, home score, date, start time, stadium address

#big_dict = []


for boxscore in boxscore_links:
    r = requests.get(boxscore)
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
        start_time_strong_tag = soup.find('strong', text="Start Time")
        start_time_text = start_time_strong_tag.next_sibling.strip('" ')[2:]

        #stadium
        #do we want the stadium name or the link to the page of the stadium which has the address
        stadium_name = soup.find('strong', text='Stadium')
        stadium_href = stadium_name.next_sibling.next_sibling.get('href')
        stadium_link = f'https://www.pro-football-reference.com{stadium_href}'

        #using stadium link to get zip code of stadium
        r = requests.get(stadium_link)
        if (r.status_code == 200):
            soup = BeautifulSoup(r.content, 'html.parser')
            meta_div = soup.find('div', id='meta')
            address_p = meta_div.find('p')
            zipcode = address_p.get_text()[-5:]

            #print(address_text)

        else:
            print("Failed to retrieve the webpage")


        game_info = [scores[0], scores[1], date_text, start_time_text, zipcode]

        print(game_info)

    else:
        print("Failed to retrieve the webpage")









