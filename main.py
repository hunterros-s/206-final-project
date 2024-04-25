from weather import get_icao_code, get_weather
from sports import get_game_links, get_all_boxscores
from utils import datetime_location_to_epoch
from database import get_db, create_games_table, insert_data

def main():
    conn, cursor = get_db("data.db")

    create_games_table(cursor)

    year = 2019
    week = 2

    success, links = get_game_links(year, week)

    if not success:
        print("get game links did not work")
        quit()

    week_info = get_all_boxscores(links)
    week_info_for_db = []
    for info in week_info:
        away_name, away_score, home_name, home_score, date, time, location = info
        unix_time = datetime_location_to_epoch(date, time, location)
        week_info_for_db.append(
            (away_name, away_score, home_name, home_score, unix_time, year, week, date, time, location)
        )
    
    for week_info in week_info_for_db:
        insert_data(conn, cursor, week_info)
    
    

if __name__ == "__main__":
    main()