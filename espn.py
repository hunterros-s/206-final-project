from collections import namedtuple
import requests

def get_event_links(year, week):
    base = "https://sports.core.api.espn.com"
    api_url = f"/v2/sports/football/leagues/nfl/seasons/{year}/types/2/weeks/{week}/events?lang=en&region=us"

    try:
        output = requests.get(base + api_url)
        output.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []
    
    data = output.json()

    link_list = data.get("items")

    links = []

    for dict in link_list:
        link = dict.get("$ref")

        links.append(link)

    return links

def get_football_event_info(link):
    try:
        output = requests.get(link)
        output.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return ()

    data = output.json()

    ref_link = data.get("$ref")
    id = data.get("id")
    datetime = data.get("date")
    name = data.get("name")

    competitions = data.get("competitions")[0]

    attendance = competitions.get("attendance")

    venue = competitions.get("venue")

    grass = venue.get("grass")
    indoor = venue.get("indoor")

    address_obj = venue.get("address")
    city = address_obj.get('city')
    state = address_obj.get('state')
    zip = address_obj.get('zipCode')

    address = f"{city}, {state} {zip}"

    if city is None or state is None or zip is None:
        raise Exception(f"invalid address: {address}")

    return (ref_link, id, datetime, name, attendance, grass, indoor, address)

# https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401326315
def get_more_football_data(id):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={id}"

    try:
        output = requests.get(url)
        output.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return ()

    data = output.json()

    boxscore = data.get("boxscore")

    teams = boxscore.get("teams")

    first_team = teams[0]
    second_team = teams[1]

    first_team_stats = first_team.get("statistics")
    second_team_stats = second_team.get("statistics")

    first_team_completionAttempts = first_team_stats[11].get("displayValue")
    second_team_completionAttempts = second_team_stats[11].get("displayValue")

    players = boxscore.get("players")
    first_players = players[0]
    second_players = players[1]

    first_players_stats = first_players.get("statistics")
    second_players_stats = second_players.get("statistics")

    first_kicking_stats = first_players_stats[8]
    second_kicking_stats = second_players_stats[8]

    first_kicking_totals = first_kicking_stats.get("totals")
    second_kicking_totals = second_kicking_stats.get("totals")

    if len(first_kicking_totals) != 0:
        first_kicking_FG = first_kicking_totals[0]
        first_kicking_LONG = first_kicking_totals[2]
    else:
        first_kicking_FG = "0/0"
        first_kicking_LONG = "0"

    if len(second_kicking_totals) != 0:
        second_kicking_FG = second_kicking_totals[0]
        second_kicking_LONG = second_kicking_totals[2]
    else:
        second_kicking_FG = "0/0"
        second_kicking_LONG = "0"

    return (first_team_completionAttempts, second_team_completionAttempts, first_kicking_FG, first_kicking_LONG, second_kicking_FG, second_kicking_LONG)


def get_game_info(link):
    FootballEventInfo = namedtuple('FootballEventInfo', ['ref_link', 'id', 'datetime', 'name', 'attendance', 'grass', 'indoor', 'address'])
    FootballData = namedtuple('FootballData', ['first_team_completionAttempts', 'second_team_completionAttempts', 'first_kicking_FG', 'first_kicking_LONG', 'second_kicking_FG', 'second_kicking_LONG'])

    try:
        event_info = FootballEventInfo(*get_football_event_info(link))
        more_data = FootballData(*get_more_football_data(event_info.id))
    except Exception as e:
        print(link)
        raise Exception(f"Error: {e}")

    data = (
        event_info.id,
        event_info.ref_link,
        event_info.datetime,
        event_info.name,
        event_info.attendance,
        event_info.grass,
        event_info.indoor,
        event_info.address,
        more_data.first_team_completionAttempts,
        more_data.second_team_completionAttempts,
        more_data.first_kicking_FG,
        more_data.first_kicking_LONG,
        more_data.second_kicking_FG,
        more_data.second_kicking_LONG
    )

    return data


#https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2003/types/2/weeks?lang=en&region=us
def get_weeks(year):
    url = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/types/2/weeks?lang=en&region=us"

    try:
        output = requests.get(url)
        output.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return ()
    
    data = output.json()

    return data.get("count", 0)