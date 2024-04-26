import sqlite3

def get_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
    except Exception as e:
        print(e)

    return conn, cursor


def create_weather_table(cursor):
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wind_speed INTEGER,
            temperature INTEGER,
            condition TEXT,
            UNIQUE(wind_speed, temperature, condition)
        )
        ''')
    except Exception as e:
        print(e)


def create_games_table(cursor):
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            ref_link TEXT,
            datetime TEXT,
            name TEXT,
            attendance INTEGER,
            grass INTEGER,
            indoor INTEGER,
            address TEXT,
            first_team_completionAttempts TEXT,
            second_team_completionAttempts TEXT,
            first_kicking_FG TEXT,
            first_kicking_LONG INTEGER,
            second_kicking_FG TEXT,
            second_kicking_LONG INTEGER,
            weather_id INTEGER,
            FOREIGN KEY(weather_id) REFERENCES weather(id)
        )
        ''')
    except Exception as e:
        print(e)

def get_outdoor_events(cursor):
    try:
        cursor.execute('''
            SELECT * FROM games WHERE INDOOR = 0
        ''')
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)


def check_exist(cursor, id):
    cursor.execute("SELECT count(*) FROM games WHERE id = ?", (id,))

    count = cursor.fetchone()[0]

    return count != 0


def insert_data(conn, cursor, data):
    cursor.execute('''
        INSERT OR IGNORE INTO games
        (id, ref_link, datetime, name, attendance, grass, indoor, address,
         first_team_completionAttempts, second_team_completionAttempts,
         first_kicking_FG, first_kicking_LONG, second_kicking_FG, second_kicking_LONG)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    
def get_set_weather(conn, cursor, wind_speed, temperature, condition):
    cursor.execute('''
        INSERT OR IGNORE INTO weather (wind_speed, temperature, condition) VALUES (?, ?, ?);
    ''', (wind_speed, temperature, condition))
    cursor.execute('''
        SELECT id FROM weather WHERE wind_speed = ? AND temperature = ? AND condition = ?
    ''', (wind_speed, temperature, condition))
    row_id = cursor.fetchone()[0]
    conn.commit()
    return row_id

def set_weather_id(conn, cursor, id, weather_id):
    cursor.execute('''
        UPDATE games
        SET weather_id = ?
        WHERE id = ?;
    ''', (weather_id, id))
    conn.commit()