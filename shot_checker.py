import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time

def get_match_url(Week):
    # The link to get premier league data
    url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
    base_url = "https://fbref.com"
    
    # Sort out the DataFrame
    df = pd.read_html(url)[0]
    df = pd.read_html(url, extract_links = 'body')[0]
    df = df.apply(lambda col: [v[0] if v[1] is None else f'{base_url}{v[1]}' for v in  col])
    df['Wk'] = pd.to_numeric(df['Wk'], errors='coerce')
    
    # Only keep the Week and the Match Report Link
    df = df[['Wk','Match Report']]

    # Select which week
    df = df[df['Wk'] == Week]
    #print(df)
    return df

#get_match_url(26)

def find_player_shots(week):
    # Get the DataFrame from the above function
    df = get_match_url(week)
    players_over_two_shots = []
    for index, row in df.iterrows():
        url = row['Match Report']
        if url:
            home_table = pd.read_html(url)[3]
            home_table.columns = home_table.columns.droplevel(0)
            home_table = home_table[['Player', 'Sh']]
            home_table = home_table[home_table['Sh'] > 2]
            home_table = home_table.drop(home_table.index[-1])

            away_table = pd.read_html(url)[10]
            away_table.columns = away_table.columns.droplevel(0)
            away_table = away_table[['Player', 'Sh']]
            away_table = away_table[away_table['Sh'] > 2]
            #away_table = away_table.drop(away_table.index[-1])

            # Append DataFrames to the list
            if not home_table.empty:
                players_over_two_shots.append(home_table)
            if not away_table.empty:
                players_over_two_shots.append(away_table)
            time.sleep(5)

    #print(players_over_two_shots)
    return players_over_two_shots
        

#find_player_shots(27)

output_folder = "Player Shots"

def create_spreadsheet(week):
    df = find_player_shots(week)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    df = pd.concat(df, ignore_index=True)
    
    df.to_csv(os.path.join(output_folder, f'Gameweek {week}.csv'), index=False)

create_spreadsheet(24)


