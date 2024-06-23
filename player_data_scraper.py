import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

def get_team_url(team_name):
    # This is for the premier league
    premier_league_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
   
    # Send request to the URL
    response = requests.get(premier_league_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # ID of table we want
    table = soup.find('table', {'id': 'results2023-202491_overall'})

    # // Find all team names in the table and print them
    team_names = []
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) > 1:
            team_names.append(columns[1].text.strip())
    
    # Extract hyperlinks from table
    for link in table.find_all('a'):
        href = link.get('href')
        if href and '/en/squads' in href and team_name in link.text:
            return f'https://fbref.com{href}'
        
    # Failsafe if team not found
    print('Team not found')
    return None

url = get_team_url('Liverpool')

def stat_finder(team_name):
    team_url = get_team_url(team_name)
    
    # Choose specific table from team url (5 = passing | 0 = standard stats | 4 = shooting stats)
    df = pd.read_html(team_url)[4]
    df.columns = df.columns.droplevel(0)
    #df = df[df['MP'] > 15] 
    df = df[df['90s'] > 10]

    # Filter number of shots if necessary
    df = df[df['Sh'] > 10]
    df = df.iloc[:-2]

    # Drop final column
    df = df.iloc[:, :-1]

    df = df.drop(['Nation','Pos','Age'],axis=1)
    
    #df = df[['Player','KP','Ast','xAG','xA','1/3','PPA','PrgP']]
    #print(df.columns)
    return df

output_folder = "Premier League 200224 shots"

def create_spreadsheet(team_name):
    df = stat_finder(team_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    df.to_csv(os.path.join(output_folder, f'{team_name}.csv'), index=False)

#print(stat_finder('Liverpool'))
#table = stat_finder('Liverpool')
#print(table)

#create_spreadsheet("Sheffield Utd")
#print(stat_finder('Liverpool'))


teams = ["Liverpool",
         "Manchester City",
         "Arsenal",
         "Tottenham",
         "Aston Villa",
         "Manchester Utd",
         "Newcastle Utd",
         "West Ham",
         "Brighton",
         "Chelsea",
         "Wolves",
         "Fulham",
         "Bournemouth",
         "Brentford",
         "Crystal Palace",
         "Nott'ham Forest",
         "Luton Town",
         "Everton",
         "Burnley",
         "Sheffield Utd"]


def create_spreadsheets_for_teams(teams):
    for team_name in teams:
        create_spreadsheet(team_name)

create_spreadsheets_for_teams(teams)








