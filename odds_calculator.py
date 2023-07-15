import pandas as pd
import matplotlib.pyplot as plt

table = pd.read_csv('Champ21-22.csv')

omit = ['Div', 'Date', 'Time','HTHG','HTAG','HTR','Referee',
        'HS','AS','HST','AST','HF','AF','HC','AC','HY',
        'AY','HR','AR']

rename = {
    'FTR':'Result', 'FTHG':'Home', 'FTAG':'Away'}

table = table.drop(columns=omit)
table = table.rename(columns=rename)

cutoff = 'B365A'
index = table.columns.get_loc(cutoff)

table = table.iloc[:, :index + 1]

results_column = 'Result'
odds_columns = ['B365H','B365D','B365A']
#odds_columns = ['PSH','PSD','PSA']
table['specified odds'] = ''

for index, row in table.iterrows():
    result = row[results_column]
    
    for odd in odds_columns:
        last_letter = odd[-1]
        odds_value = row[odd]
        
        if last_letter.lower() == result.lower():
            table.at[index, 'specified odds'] = odds_value
            break

bet = 5

table['Min odds'] = table[['B365H','B365D','B365A']].max(axis=1)
table['Favourite'] = table['Min odds'].astype(float) * bet - bet

table['final profit'] = table.apply(
    lambda row: row['Favourite'] if row['Min odds'] == row['specified odds'] else -bet,
    axis=1
)
        
total_profit = table['final profit'].sum()

table['Cumulative'] = table['final profit'].cumsum()

plt.plot(table['Cumulative'])
plt.xlabel('Match')
plt.ylabel('Cumulative Profit/Loss')
plt.title('Favourite Betting 22/23')
plt.show()

"""Betting on the favourite with Bet 365, £5 at a time returns £23.20
   Betting on the underdog nets -£55"""
   


