import pandas as pd
import requests
from bs4 import BeautifulSoup
from IPython.display import display

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
    
    df = pd.read_html(team_url)[0]
    df.columns = df.columns.droplevel(0)
    df = df[df['MP'] > 2] 
    df = df.iloc[:-2]

    df = df.drop(['Nation','Pos','Age'],axis=1)
    
    return df

def create_spreadsheet(team_name):
    df = stat_finder(team_name)
    df.to_csv(f'{team_name}.xlsx', index=False)

#print(stat_finder('Liverpool'))
#table = stat_finder('Liverpool')

create_spreadsheet('Liverpool')










