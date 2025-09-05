from pathlib import Path

from psycopg2.extras import execute_values

import utilities

TEAMS_FILE = Path("./teams/teams.json")

def insert_teams_data(data):
    conn = utilities.get_database_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO teams 
    (
        team_id,
        franchise_id,
        full_name,
        tri_code
    ) 
    VALUES %s
    ON CONFLICT(team_id) DO NOTHING;"""

    # loads all data in 1 trip
    execute_values(cur, insert_query, data)

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()


def extract_teams_fields(raw_teams_data):
    teams = [
        (
            team["id"],
            team["franchiseId"],
            team["fullName"],
            team["triCode"],
        )
        for team in raw_teams_data
    ]
    return teams

def run_pipeline():
    raw_teams_data = utilities.read_from_file(TEAMS_FILE)
    processed_teams_data = extract_teams_fields(raw_teams_data)
    insert_teams_data(processed_teams_data)


if __name__ == "__main__":
    run_pipeline()