import time
import re

from weather import get_icao_code, get_weather
from utils import datetime_location_to_epoch
from database import get_db, create_games_table, insert_data, check_exist
from espn import get_event_links, get_more_football_data, get_football_event_info, get_weeks, get_game_info



# we should make flags which run the program. so liek --nfl --year 2006 starts the data scraping. --weather gets the data --viz visualizes the data

def main():
    conn, cursor = get_db("data.db")

    create_games_table(cursor)

    years = range(2006, 2024)
    for year in years:
        print(f"starting year: {year}")
        week_count = get_weeks(year)
        weeks = range(1, 1 + week_count)
        for week in weeks:
            print(f"starting week {week}")
            events = get_event_links(year, week)
            for link in events:

                id = re.search('events\/(\d+)', link).group(1)
                if check_exist(cursor, id):
                    continue
                
                try:
                    data = get_game_info(link)
                except Exception as e:
                    print(f"exception: {e}")
                    continue
                print(data)
                insert_data(conn, cursor, data)

if __name__ == "__main__":
    main()