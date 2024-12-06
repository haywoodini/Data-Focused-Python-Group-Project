import pandas as pd
import os
import numpy as np

def data_pipeline():
    file_paths = ["amazon_pet_food.csv"]

    dataframes = []
    for file_path in file_paths:
        df = extract_data(file_path)
        dataframes.append(df)

    transformed_data = transform_data(dataframes)

    load_data(transformed_data, "amazon_cleaned.csv")

def extract_data(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print(f"Successfully extracted data from {file_path}")
        return df
    else:
        print(f"File not found: {file_path}")
        return pd.DataFrame()

def transform_data(dataframes):
    all_data = pd.concat(dataframes, axis=0, ignore_index=True)  # 合并所有数据

    all_data['Brand'] = all_data['Brand'].apply(standardize_brand)

    all_data['Price($)'] = all_data['Price'].apply(clean_price)

    all_data['Price($)'].fillna("Price unavailable", inplace=True)

    all_data['Sales(last month)'] = all_data['Sales'].apply(clean_sales)

    all_data['Rating'] = all_data['Rating'].apply(clean_rating)

    all_data.drop(columns=['Price', 'Sales'], inplace=True)
    all_data.dropna(inplace=True)
    all_data.drop_duplicates(inplace=True)

    print("Data transformation completed.")
    return all_data

def standardize_brand(brand):
    if pd.isna(brand):
        return brand
    brand_lower = brand.lower()
    if "hill's" in brand_lower:
        return "Hill's"
    elif brand_lower.startswith("iams"):
        return "Iams"
    elif brand_lower.startswith("nutro"):
        return "Nutro"
    elif brand_lower.startswith("purina"):
        return "Purina"
    return brand

def clean_price(price):
    if price == "$." or pd.isna(price):
        return np.nan
    cleaned_price = price.replace("$", "").strip()
    try:
        return float(cleaned_price)
    except ValueError:
        return np.nan

def clean_sales(sales):
    if pd.isna(sales):
        return "Sales unavailable"
    cleaned_sales = sales.replace(" bought in past month", "").strip()
    return cleaned_sales if cleaned_sales else "Sales unavailable"

def clean_rating(rating):
    if pd.isna(rating):
        return np.nan
    try:
        return float(rating.split(" out of ")[0]
    except ValueError:
        return np.nan


def load_data(data, output_path):
    data.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Data has been loaded to '{output_path}'")

# Main Pipeline
if __name__ == "__main__":
    data_pipeline()
