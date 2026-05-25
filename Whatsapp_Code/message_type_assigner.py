#Assings a message type (Personalised or Basic) to each contact. 
import csv
import random
import pandas as pd

# Read the CSVs and assign Custom or Basic randomly. Each CSV has two groups: CloseFriends=Yes or No. I want each group to be balanced.
csvs = ["friends_code.csv", "friends2_code.csv", "friends3_code.csv"]

for csv in csvs:
    df = pd.read_csv(csv)
    # Divide into two groups
    grupo_yes = df[df['CloseFriends'] == 'Yes']
    grupo_no = df[df['CloseFriends'] == 'No']
    
    # Randomly assign Custom or Basic to each group
    opciones = ['Personalised', 'Basic']
    
    df.loc[grupo_yes.index, 'MessageType'] = random.choices(opciones, k=len(grupo_yes))
    df.loc[grupo_no.index, 'MessageType'] = random.choices(opciones, k=len(grupo_no))
    
    # Save the modified CSV file
    df.to_csv(csv.replace('.csv', '_assigned.csv'), index=False, encoding='utf-8')
    print(f"✅ It was assigned 'MessageType' to {len(df)} contacts in {csv}.")
