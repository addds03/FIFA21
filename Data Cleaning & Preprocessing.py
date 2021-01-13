"""
Created on Mon Jan 11 17:24:47 2021

@author: aditya
"""
import pandas as pd

df_fifa = pd.read_csv('fifa21_male2.csv')

# Created a copy in case I screw with the dataset (my preference)
df_fifa_copy = df_fifa.copy()

# Removed extra information from the columns (such as *)
df_fifa_copy['W/F'] = df_fifa_copy['W/F'].apply(lambda x: x.split(' ')[0])
df_fifa_copy['IR'] = df_fifa_copy['IR'].apply(lambda x: x.split(' ')[0])
df_fifa_copy['SM'] = df_fifa_copy['SM'].apply(lambda x: x[0][0])

# Inserted value for BP when Position is null
df_fifa_copy['Position'] = df_fifa_copy['Position'].fillna(0)
df_fifa_copy['Position'] = df_fifa_copy.apply(lambda x: x['BP'] if x['Position'] == 0 else x['Position'], axis = 1)

# Dropped unnecessary columns 'LS through - GK' & Team contract and Loan Date End
df_fifa_copy.drop(df_fifa_copy.columns[79:-1],axis=1,inplace=True)
df_fifa_copy.drop(columns=['Team & Contract','Loan Date End'], axis=1, inplace=True)

# Created free agent column
df_fifa_copy['Free agent'] = df_fifa_copy['Contract'].apply(lambda x: 1 if 'free' in x.lower() else 0)

# Created column to indicate a retired player
df_fifa_copy['Retired'] = df_fifa_copy.apply(lambda x: 1 if '~' not in x['Contract'].lower() and x['Free agent'] != 1 else 0,axis = 1)

# Created Contract end column
df_fifa_copy['Contract end'] = df_fifa_copy.apply(lambda x: x['Contract'].split(' ~ ')[1] if x['Free agent'] != 1 and x['Retired'] != 1 else 0, axis = 1)

# Replaced &amp; junk character with & in the Nationality column
df_fifa_copy['Nationality'] = df_fifa_copy['Nationality'].apply(lambda x: x.replace('&amp;','&'))

# Checked for player versatility/ number of position on which player can play
df_fifa_copy['Player Positions'] = df_fifa_copy['Position'].apply(lambda x: len(x.split()))

# Removed lbs from weight to make it numerical
df_fifa_copy['Weight'] = df_fifa_copy['Weight'].apply(lambda x:x.replace('lbs',''))

# Function converts string currency values to numerical values (i.e $150k to 150000)
def currencytonumber(currency):
    currency_temp = currency.lower().replace('€','').replace('k','').replace('m','')
    
    if 'K' in currency:
        return int(1000 * float(currency_temp))
    elif 'M' in currency:
        return int(1000000 * float(currency_temp))
    else:
        return int(0)
    
# Convert Value, Wage & Release Clause to numerical values
df_fifa_copy['Value'] = df_fifa_copy['Value'].apply(currencytonumber)
df_fifa_copy['Wage'] = df_fifa_copy['Wage'].apply(currencytonumber)
df_fifa_copy['Release Clause'] = df_fifa_copy['Release Clause'].apply(currencytonumber)

df_fifa = df_fifa_copy.copy()

df_fifa.to_csv('fifa21_cleaned.csv',index=False)


# If contract ends in 2020 as well as free agent and retired is 0
#df_fifa_copy['Free agent'] = df_fifa_copy.apply(lambda x: 1 if x['Contract end'] == 2020 and x['Retired'] == 0 and x['Free agent'] == 0 else 0, axis=1)

# If contract ends before 2021 as well as free agent and retired is 0
#df_fifa_copy['Retired'] = df_fifa_copy.apply(lambda x: 1 if x['Contract end'] < 2021 and x['Retired'] == 0 and x['Free agent'] == 0 else 0, axis=1) 
