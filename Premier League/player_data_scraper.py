import pandas as pd
import requests
from bs4 import BeautifulSoup
from IPython.display import display
import time

def get_team_url(team_name):
    # This is for the premier league
    premier_league_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    time.sleep(3) 
    tables = pd.read_html(premier_league_url)[0]
    #print(tables)
    
    # Send request to the URL
    response = requests.get(premier_league_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    
    # ID of table we want
    #table = soup.find('table', {'id': 'results2023-202491_overall'})
    table = soup.find('table', {'id': 'results2023-202491_overall'})
    
    # Extract hyperlinks from table
    if table:
        for link in table.find_all('a'):
            href = link.get('href')
            if href and '/en/squads' in href and team_name in link.text:
               return f'https://fbref.com{href}'
        
    # Failsafe if team not found
    print('Team not found')
    return None

def stat_finder(team_name):
    team_url = get_team_url(team_name)
    
    df = pd.read_html(team_url)[0]
    df.columns = df.columns.droplevel(0)
    df = df[df['MP'] > 2] 
    df = df.iloc[:-2]

    df = df.drop(['Nation','Pos','Age'],axis=1)
    df = df[['Player','PrgC','PrgP', 'PrgR','Min','npxG+xAG']]
    
    return df

def create_spreadsheet(team_name):
    df = stat_finder(team_name)
    df.to_csv(f'{team_name}.csv', index=False)

squads = [['Manchester City'], ['Tottenham'], ['Liverpool'], ['West Ham'], ['Arsenal'], ['Brighton'], ['Crystal Palace'], ['Brentford'], ["Nott'ham Forest"], ['Aston Villa'], ['Manchester Utd'], ['Chelsea'], ['Fulham'], ['Newcastle Utd'], ['Wolves'], ['Bournemouth'], ['Sheffield Utd'], ['Everton'], ['Luton Town'], ['Burnley']]


print(stat_finder('Liverpool'))

#if __name__ == '__main__':
#    for team in squads:
#        create_spreadsheet(team[0])

