import requests
import utilities

TEAMS_FILE_NAME = "./teams/teams.json"


def get_teams():
    url = "https://api.nhle.com/stats/rest/en/team"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]
    print(f"{response.status_code} - {response.reason}")
    return {}


def read_teams_from_file():
    return utilities.read_from_file(TEAMS_FILE_NAME)


def run_pipeline():
    teams = get_teams()
    utilities.write_to_file(TEAMS_FILE_NAME, teams)


if __name__ == "__main__":
    run_pipeline()