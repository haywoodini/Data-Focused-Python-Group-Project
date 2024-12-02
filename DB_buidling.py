import sqlite3
import pandas as pd

csv_file_path = 'amazon_cleaned.csv'
df = pd.read_csv(csv_file_path)

# Create the database as pet_food.db if not exists
conn = sqlite3.connect('pet_food.db')

# Write into the db as amazon_data
df.to_sql('amazon_data', conn, if_exists='replace', index=False)
conn.close()
