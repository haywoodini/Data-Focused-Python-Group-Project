import streamlit as st
import pandas as pd

# Load data from CSV files
amazon_csv_path = 'amazon_cleaned.csv'
reddit_csv_path = 'reddit_cleaned.csv'
manufacturer_csv_path = 'pet_manufactuer_rank_subbrand.csv'

# Read CSV files into Pandas DataFrames
amazon_df = pd.read_csv(amazon_csv_path)
reddit_df = pd.read_csv(reddit_csv_path)
manufacturer_df = pd.read_csv(manufacturer_csv_path)

# Clean column names
amazon_df.columns = amazon_df.columns.str.strip()
reddit_df.columns = reddit_df.columns.str.strip()
manufacturer_df.columns = manufacturer_df.columns.str.strip()

# Standardize brand names
amazon_df['Brand'] = amazon_df['Brand'].str.strip().str.lower()
reddit_df['Brand'] = reddit_df['Brand'].str.strip().str.lower()
manufacturer_df['Subbrand'] = manufacturer_df['Subbrand'].str.strip().str.lower()

# Convert Price($) column to numerical
amazon_df['Price($)'] = pd.to_numeric(amazon_df['Price($)'], errors='coerce')

# Perform left joins on the DataFrames
joined_df = amazon_df.merge(reddit_df[['Brand', 'Average_Sentiment_Score']], on='Brand', how='left')
joined_df.rename(columns={'Average_Sentiment_Score': 'Average_Score_Reddit'}, inplace=True)

joined_df = joined_df.merge(manufacturer_df[['Subbrand', 'Rank']], left_on='Brand', right_on='Subbrand', how='left')
joined_df.rename(columns={'Rank': 'manu_sale_rank'}, inplace=True)
joined_df.drop(columns=['Subbrand'], inplace=True)

# Streamlit UI
def main():
    st.title("Pet Food Recommendation System")
    st.sidebar.header("Filter Criteria")

    # Option settings for user input
    pet_type = st.sidebar.selectbox("Pet Type", ("Any", "Dog", "Cat"))
    brand = st.sidebar.text_input("Brand (e.g., Hill's, Purina)")
    min_price = st.sidebar.number_input("Minimum Price ($)", min_value=0.0, step=1.0)
    max_price = st.sidebar.number_input("Maximum Price ($)", min_value=0.0, step=1.0)
    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 4.0, 0.1)
    ingredients_needed = st.sidebar.text_input("Ingredients Needed (comma separated)")
    ingredients_not_needed = st.sidebar.text_input("Ingredients Not Needed (comma separated)")

    sort_by = st.sidebar.selectbox("Sort by", ("Rating", "Price($)", "No Sort"))
    sort_order = st.sidebar.radio("Sort Order", ("Ascending", "Descending"))

    if st.sidebar.button("Search"):
        # Create a copy of the DataFrame to filter
        filtered_df = joined_df.copy()

        # Filter based on user inputs
        if pet_type != "Any":
            filtered_df = filtered_df[filtered_df['Product'].str.lower().str.contains(pet_type.lower())]

        if brand:
            filtered_df = filtered_df[filtered_df['Brand'].str.contains(brand.strip().lower())]

        if min_price > 0:
            filtered_df = filtered_df[filtered_df['Price($)'] >= min_price]

        if max_price > 0:
            filtered_df = filtered_df[filtered_df['Price($)'] <= max_price]

        if min_rating > 0:
            filtered_df = filtered_df[filtered_df['Rating'] >= min_rating]

        if ingredients_needed:
            needed_list = [ingredient.strip().lower() for ingredient in ingredients_needed.split(',')]
            for ingredient in needed_list:
                filtered_df = filtered_df[filtered_df['Ingredients'].str.lower().str.contains(ingredient)]

        if ingredients_not_needed:
            not_needed_list = [ingredient.strip().lower() for ingredient in ingredients_not_needed.split(',')]
            for ingredient in not_needed_list:
                filtered_df = filtered_df[~filtered_df['Ingredients'].str.lower().str.contains(ingredient)]

        # Sort the data
        if sort_by != "No Sort":
            ascending = True if sort_order == "Ascending" else False
            filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

        # Display results
        if not filtered_df.empty:
            st.write(f"Found {len(filtered_df)} product link{'s' if len(filtered_df) > 1 else ''}")
            st.write(filtered_df)
        else:
            st.write("No products found with the specified criteria.")

if __name__ == "__main__":
    main()




