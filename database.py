import sqlite3

def get_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
    except Exception as e:
        print(e)

    return conn, cursor

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
            second_kicking_LONG INTEGER
        )
        ''')
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
    