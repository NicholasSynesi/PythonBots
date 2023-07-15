import pandas as pd

# Choose league
url = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'
league_list = []

league_list.append(pd.read_html(url, index_col=False, flavor='lxml')[0])
league_list = pd.concat(league_list, axis=0, ignore_index=True)

# First, make an average of home xG vs away xG

league_df = league_list[league_list['Wk'].notna()]

league_df = league_df.rename(columns={'xG':'xGHome'
                   ,'xG.1':'xGAway'})

league_df['HomeScore'] = pd.to_numeric(league_df['Score'].str[0], errors='coerce')
league_df['AwayScore'] = pd.to_numeric(league_df['Score'].str[2], errors='coerce')
#league_df['HomeScore'] = league_df['Score'].str[0]
#league_df['AwayScore'] = league_df['Score'].str[2]

league_df = league_df.drop(['Match Report', 'Notes'],axis=1)

league_df['Date'] = pd.to_datetime(league_df['Date'])

league_df.sort_values(by='Date', inplace=True)

league_df = league_df[['Wk','Day','Date','Time','Home',
                       'HomeScore','xGHome','AwayScore',
                       'xGAway','Away','Attendance','Venue','Referee']]

league_df = league_df.dropna()

league_df = league_df[['Date','Home','HomeScore','xGHome',
                       'AwayScore','xGAway','Away', 'Referee']].reset_index(drop=True)

league_Mean_Home_xG = round((league_df['xGHome'].mean()),2)
league_Mean_Away_xG = round((league_df['xGAway'].mean()),2)

league_Avg_Home_Goals = round(league_df['HomeScore'].mean(), 2)
league_Avg_Away_Goals = round(league_df['AwayScore'].mean(), 2)

"""Note to self, average home xG is 1.58, away is 1.26"""



