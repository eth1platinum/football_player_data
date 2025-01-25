# libraries
import pandas as pd

# fbref table link
url_df = 'https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats#stats_gca'

df = pd.read_html(url_df)[0]
# creating a data with the same headers but without multi indexing
df.columns = [' '.join(col).strip() for col in df.columns]

df = df.reset_index(drop=True)

# creating a list with new names
new_columns = []
for col in df.columns:
  if 'level_0' in col:
      new_col = col.split()[-1]  # takes the last name
  else:
      new_col = col
  new_columns.append(new_col)

# rename columns
df.columns = new_columns
df = df.fillna(0)

df['Age'] = df['Age'].str[:2]
df['Position_2'] = df['Pos'].str[3:]
df['Position'] = df['Pos'].str[:2]
df['Nation'] = df['Nation'].str.split(' ').str.get(1)
df['League'] = df['Comp'].str.split(' ').str.get(1)
df['League_'] = df['Comp'].str.split(' ').str.get(2)
df['League'] = df['League'] + ' ' + df['League_']
df = df.drop(columns=['League_', 'Comp', 'Rk', 'Pos','Matches'])

df['Position'] = df['Position'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})
df['Position_2'] = df['Position_2'].replace({'MF': 'Midfielder', 'DF': 'Defender',
                                                 'FW': 'Forward', 'GK': 'Goalkeeper'})
df['League'] = df['League'].fillna('Bundesliga')

counter = 0 # get 16 and under players
for age in df['Age']:
    try:
        age_val = int(age)
        if age_val <= 18 and float(df['90s'][counter]) >= 5.0:
            print(df['Player'][counter])
        counter = counter + 1
    except ValueError:
        counter = counter + 1
        continue

# counter = 0 # get all liverpool players
# for team in df['Squad']:
#     try:
#         if team == 'Liverpool':
#             print(df['Player'][counter])
#         counter = counter + 1
#     except ValueError:
#         counter = counter + 1
#         continue
#
#counter = 0 # get young creators
#for creation in df['SCA SCA90']:
#    try:
#        if float(creation) >= 4.0 and float(df['90s'][counter]) >= 5.0 and int(df['Age'][counter]) <= 23 and df['Position'][counter] == 'Midfielder':
#            print(df['Player'][counter])
#        counter = counter + 1
#    except ValueError:
#        counter = counter + 1
#        continue
