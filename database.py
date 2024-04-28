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
        CREATE TABLE IF NOT EXISTS condition (
            condition_id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition_text TEXT UNIQUE
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wind_speed INTEGER,
            temperature INTEGER,
            condition_id INTEGER,
            UNIQUE(wind_speed, temperature, condition_id),
            FOREIGN KEY (condition_id) REFERENCES condition (condition_id)
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
    # First, check if the condition already exists in the condition table.
    cursor.execute('''
        SELECT condition_id FROM condition WHERE condition_text = ?;
    ''', (condition,))
    result = cursor.fetchone()

    # If the condition does not exist, insert it.
    if result is None:
        cursor.execute('''
            INSERT INTO condition (condition_text) VALUES (?);
        ''', (condition,))
        condition_id = cursor.lastrowid
    else:
        condition_id = result[0]

    # Now that we have the condition_id, we can insert or ignore into the weather table.
    cursor.execute('''
        INSERT OR IGNORE INTO weather (wind_speed, temperature, condition_id) VALUES (?, ?, ?);
    ''', (wind_speed, temperature, condition_id))
    cursor.execute('''
        SELECT id FROM weather WHERE wind_speed = ? AND temperature = ? AND condition_id = ?;
    ''', (wind_speed, temperature, condition_id))
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

def join_games_weather(cursor):
    cursor.execute('''
        SELECT
            games.*,
            weather.id AS weather_id,
            weather.wind_speed,
            weather.temperature,
            condition.condition_text
        FROM games
        INNER JOIN weather
            ON games.weather_id = weather.id
        INNER JOIN condition
            ON weather.condition_id = condition.condition_id
    ''')
    results = cursor.fetchall()
    return results