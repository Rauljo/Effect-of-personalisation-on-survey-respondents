#Reads friends list and assigns a unique code to each contact in a new column called "code"
import pandas as pd

csvs = ["friends.csv", "friends2.csv", "friends3.csv"]

#lengths:
lengths = [len(pd.read_csv(csv)) for csv in csvs]

start = 0
for i, csv in enumerate(csvs):
    df = pd.read_csv(csv)
    df['code'] = range(start, start + lengths[i])
    start += lengths[i]
    #We save it with the same name + "_code"
    df.to_csv(csv.replace('.csv', '_code.csv'), index=False, encoding='utf-8')
    print(f"✅ Code column was added to {len(df)} contacts in {csv}.")
