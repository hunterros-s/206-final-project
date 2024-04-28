import time
import re
import argparse

from weather import get_icao_code, get_weather
from utils import ISO_8601_to_datetime
from database import get_db, create_games_table, insert_data, check_exist, create_weather_table, get_outdoor_events, get_set_weather, set_weather_id, join_games_weather
from espn import get_event_links, get_weeks, get_game_info
from visualizations import make_graphics



# we should make flags which run the program. so liek --nfl --year 2006 starts the data scraping. --weather gets the data --viz visualizes the data

parser = argparse.ArgumentParser(prog='SI206 final project',
                                description='gets weather and sports evetns and graphs')
parser.add_argument('-e', '--espn', type=int, help="Set the ESPN value, default is 25. Can be changed to a bigger integer.")
parser.add_argument('-w', '--weather', type=int, help="Set the Weather value, default is 25. Need ESPN data first. Can be changed to a bigger integer.")
parser.add_argument('-v', '--visual', action='store_true', help="if enabled it will get weather data and game data from db and make visualizations")

def main():
    args = parser.parse_args()

    print("Loading database")
    conn, cursor = get_db("data.db")
    create_games_table(cursor)
    create_weather_table(cursor)
    print("database loaded")

    if args.espn is not None:
        counter = 0
        years = range(2006, 2024)
        outer_break = False
        for year in years:
            if outer_break:
                break
            print(f"starting year: {year}")
            week_count = get_weeks(year)
            weeks = range(1, 1 + week_count)
            for week in weeks:
                if outer_break:
                    break
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
                    counter += 1
                    print(f"{counter}/{args.espn}: {data}")
                    insert_data(conn, cursor, data)
                    if counter == args.espn:
                        outer_break = True
                        break
        return 0
    if args.weather is not None:

        counter = 1

        results = get_outdoor_events(cursor)
        for result in results:
            id, ref, iso, name, attendance, grass, indoor, location, first_team_comp, second_teamp_comp, first_kicking_fg, first_kicking_long, second_kicking_fg, second_kicking_long, weather_id = result

            if weather_id is not None:
                continue

            dt = ISO_8601_to_datetime(iso)

            print(f"{counter}/{args.weather}")

            print(f"getting weather for {location}")

            temp, wspd, condition = get_weather(location, dt)

            print(f"temp: {temp}; wspd: {wspd}; condition: {condition}")

            w_id = get_set_weather(conn, cursor, wspd, temp, condition)

            print(f"got weather id of : {w_id}")

            set_weather_id(conn, cursor, id, w_id)

            print(f"set {id}'s weather_id to {w_id}")

            if counter == args.weather:
                break
            counter += 1

        return 0

    if args.visual:
        results = join_games_weather(cursor)

        make_graphics(results)





if __name__ == "__main__":
    main()