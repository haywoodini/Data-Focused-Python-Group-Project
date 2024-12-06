import pandas as pd
import sqlite3
import os

db_path = 'pet_food.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed existing database: {db_path}")

amazon_csv_path = 'amazon_cleaned.csv'
reddit_csv_path = 'reddit_cleaned.csv'
manufacturer_csv_path = 'pet_manufactuer_rank_subbrand.csv'

amazon_df = pd.read_csv(amazon_csv_path)
reddit_df = pd.read_csv(reddit_csv_path)
manufacturer_df = pd.read_csv(manufacturer_csv_path)

amazon_df.columns = amazon_df.columns.str.strip()
reddit_df.columns = reddit_df.columns.str.strip()
manufacturer_df.columns = manufacturer_df.columns.str.strip()

amazon_df['Brand'] = amazon_df['Brand'].str.strip().str.lower()
reddit_df['Brand'] = reddit_df['Brand'].str.strip().str.lower()
manufacturer_df['Subbrand'] = manufacturer_df['Subbrand'].str.strip().str.lower()

joined_df = amazon_df.merge(reddit_df[['Brand', 'Average_Sentiment_Score']], on='Brand', how='left')
joined_df.rename(columns={'Average_Sentiment_Score': 'Average_Score_Reddit'}, inplace=True)

joined_df = joined_df.merge(manufacturer_df[['Subbrand', 'Rank']], left_on='Brand', right_on='Subbrand', how='left')
joined_df.rename(columns={'Rank': 'manu_sale_rank'}, inplace=True)
joined_df.drop(columns=['Subbrand'], inplace=True)
conn = sqlite3.connect('pet_food.db')

joined_df.to_sql(name='amazon_data', con=conn, if_exists='replace', index=False)
conn.close()

print("Database has been successfully uploaded.")



