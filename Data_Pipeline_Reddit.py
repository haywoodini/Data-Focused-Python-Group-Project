import pandas as pd
import os

# Main Pipeline
def data_pipeline():
    file_path = "reddit_pet_food_analysis.csv"
    df = extract_data(file_path)

    transformed_data = transform_data(df)

    load_data(transformed_data, "reddit_cleaned.csv")

def extract_data(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print(f"Successfully extracted data from {file_path}")
        print(f"Columns in the DataFrame: {list(df.columns)}")  # 打印列名用于调试
        return df
    else:
        print(f"File not found: {file_path}")
        return pd.DataFrame()

# Data Transformation Function
def transform_data(df):
    if 'Matched_Brands_Products' in df.columns:
        df.rename(columns={'Matched_Brands_Products': 'Brand'}, inplace=True)
    else:
        raise KeyError("Column 'Matched_Brands_Products' not found in the DataFrame")

    df['Brand'] = df['Brand'].apply(clean_brand)

    df = df[df['Brand'].str.lower() != 'puppy food']

    if 'Sentiment_Score' not in df.columns:
        raise KeyError(f"Column 'Sentiment_Score' not found in the DataFrame. Available columns: {list(df.columns)}")

    # Drop rows with missing 'Sentiment Score'
    df.dropna(subset=['Sentiment_Score'], inplace=True)

    # Convert 'Sentiment Score' to numeric (in case it's not)
    df['Sentiment_Score'] = pd.to_numeric(df['Sentiment_Score'], errors='coerce')

    # Group by 'Brand' and calculate the mean of 'Sentiment Score'
    avg_sentiment = df.groupby('Brand')['Sentiment_Score'].mean().reset_index()

    # Rename the columns for output
    avg_sentiment.rename(columns={'Sentiment_Score': 'Average Sentiment Score'}, inplace=True)

    print("Data transformation completed.")
    return avg_sentiment

# Brand Cleaning Function
def clean_brand(brand):
    if pd.isna(brand):
        return brand
    brand = brand.lower()
    if ',' in brand:
        brand = brand.split(',')[0].strip()
    # Standardize brand names
    if brand == 'chews':
        return "Stella & Chewys"
    elif brand == 'ultima':
        return "ULTIMATE PET NUTRITION"
    elif brand == 'purina beyond':
        return "Purina"
    return brand.capitalize()

def load_data(data, output_path):
    data.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Data has been loaded to '{output_path}'")

if __name__ == "__main__":
    data_pipeline()


