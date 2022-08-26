import pandas as pd


JSON_FILE = 'quotes1.json'

CSV_FILE = 'quotes1.csv'


with open(JSON_FILE, encoding='utf-8') as f:
    df = pd.read_json(f)

df.to_csv(CSV_FILE, encoding='utf-8', index=False)
