import json
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

ROSTER_DIR = Path("./rosters")


def insert_player_data(data):
    load_dotenv()
    password = os.getenv("DB_PASSWORD")

    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password=password,
    )

    cur = conn.cursor()

    # files contain rosters over many years, which will have duplicate players
    # just ignore a player if we've already loaded him
    insert_query = """
    INSERT INTO players 
    (
        player_id,
        first_name,
        last_name,
        position,
        shoots_catches,
        height_inches,
        weight_pounds,
        birth_date,
        birth_country
    ) 
    VALUES %s
    ON CONFLICT(player_id) DO NOTHING;"""

    # loads all data in 1 trip
    execute_values(cur, insert_query, data)

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()


def get_player_data_from_file(file):
    players = []
    with open(file, "r") as f:
        data = json.load(f)
        players = data.get("forwards") + data.get("defensemen") + data.get("goalies")

    return players


def extract_fields(raw_player_data):
    players = [
        (
            player["id"],
            player["firstName"]["default"],
            player["lastName"]["default"],
            player["positionCode"],
            player["shootsCatches"],
            player["heightInInches"],
            player["weightInPounds"],
            player["birthDate"],
            player["birthCountry"],
        )
        for player in raw_player_data
    ]
    return players


def run_pipeline():
    processed_player_data = []
    for file in ROSTER_DIR.glob("roster*.json"):
        print(f"Processing {file}")
        raw_player_data = get_player_data_from_file(file)
        processed_player_data = extract_fields(raw_player_data)
        insert_player_data(processed_player_data)
        print(f"Finished processing {file}")


if __name__ == "__main__":
    run_pipeline()
