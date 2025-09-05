import time

import requests

import get_teams
from utilities import write_to_file


def log_roster_data(team_code, season, roster):
    file_name = f"./rosters/roster_{team_code}_{season}.json"
    write_to_file(file_name, roster)


def get_team_roster(team_code, season):
    url = f"https://api-web.nhle.com/v1/roster/{team_code}/{season}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"{response.status_code} - {response.reason}")
    return {}


def run_pipeline(start_season, end_season):
    teams = get_teams.read_teams_from_file()
    for season_start in range(start_season, end_season + 1):
        season_str = f"{season_start}{season_start + 1}"
        for team in teams:
            team_code = team["triCode"]
            print(f"Processing season {season_str} team {team_code}")
            roster = get_team_roster(team_code, season_str)
            if roster:
                log_roster_data(team_code, season_str, roster)
            time.sleep(0.1)


if __name__ == "__main__":
    run_pipeline(2000, 2024)
