import requests
import pandas as pd
import json


API_KEY = '3924acac20e64b819ff0e17c53687d3f'
BASE_URL = "https://api.football-data.org/v4/"


def get_match_data():
    headers = {'X-Auth-Token': API_KEY}
    url = BASE_URL + 'competitions/CL/matches?season=2024'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        matches = data['matches']
        return matches
    else:
        print("Failed to get match data")
        return []
    
def preprocess_data(matches):
    match_data = []
    for match in matches:
        match_info = {
            'home_team': match['homeTeam']['name'],
            'away_team': match['awayTeam']['name'],
            'home_score': match['score']['fullTime']['home'],
            'away_score': match['score']['fullTime']['away'],
            'date': match['utcDate'],
            'season': match['season']['startDate']
        }
        match_data.append(match_info)

    df = pd.DataFrame(match_data)
    df.dropna(inplace=True)

    df['date'] = pd.to_datetime(df['date'])

    return df

def add_match_results(df):
    # Create columns to indicate win/loss/draw for home/away teams
    df['home_win'] = df['home_score'] > df['away_score']
    df['away_win'] = df['away_score'] > df['home_score']
    df['draw'] = df['home_score'] == df['away_score']
    
    return df


def streak(df, team_name, num_matches):
    teamMatches = df[(df['home_team'] == team_name) | (df['away_team'] == team_name)]
    teamMatches = teamMatches.sort_values(by=['date'], ascending=False)
    last_5_matches = teamMatches.head(num_matches)

    print(last_5_matches)
    
    wins = 0
    losses = 0
    draws = 0

    for index, match in last_5_matches.iterrows():
        if match['home_team'] == team_name and match['home_score'] > match['away_score']:
            wins += 1
        elif match['home_team'] == team_name and match['home_score'] < match['away_score']:
            losses += 1
        else:
            draws += 1
        
        if match['away_team'] == team_name and match['home_score'] > match['away_score']:
            losses += 1
        elif match['away_team'] == team_name and match['home_score'] < match['away_score']:
            wins += 1
        else:
            draws += 1

    print(f"{wins} wins in the last 5 matches for {team_name}")
    print(f"{losses} losses in the last 5 matches for {team_name}")
    print(f"{draws} draws in the last 5 matches for {team_name}")


if __name__ == "__main__":
    matches = get_match_data()
    matches_df = preprocess_data(matches)
    streak_df = streak(matches_df, 'Juventus FC', 5)
    # pd.set_option('display.max_columns', None)
    # print(matches_df.head())




