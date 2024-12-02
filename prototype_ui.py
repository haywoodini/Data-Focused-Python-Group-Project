import streamlit as st
import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect('C:/Users/11479/Desktop/95888-Data Focused Python/Group Assignment/Group Project/Pet Food Recommendation System/pet_food.db')

def main():
    # UI design
    st.title("Pet Food Recommendation System")
    st.sidebar.header("Filter Criteria")

    #Option Settings for Users
    pet_type = st.sidebar.selectbox("Pet Type", ("Any", "Dog", "Cat"))
    brand = st.sidebar.text_input("Brand (e.g., Hill's, Purina)")
    min_price = st.sidebar.number_input("Minimum Price ($)", min_value=0.0, step=1.0)
    max_price = st.sidebar.number_input("Maximum Price ($)", min_value=0.0, step=1.0)
    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 4.0, 0.1)
    ingredients_needed = st.sidebar.text_input("Ingredients Needed (comma separated)")
    ingredients_not_needed = st.sidebar.text_input("Ingredients Not Needed (comma separated)")

    if st.sidebar.button("Search"):
        # Def the SQL query
        query = "SELECT * FROM amazon_data WHERE 1=1"

        # Add conditions based on user inputs
        if pet_type != "Any":
            query += f" AND Product LIKE '%{pet_type.lower()}%'"
        if brand:
            query += f" AND Brand LIKE '%{brand}%'"
        if min_price > 0:
            query += f" AND `Price($)` >= {min_price}"
        if max_price > 0:
            query += f" AND `Price($)` <= {max_price}"
        if min_rating > 0:
            query += f" AND Rating >= {min_rating}"

        if ingredients_needed:
            needed_list = [ingredient.strip() for ingredient in ingredients_needed.split(',')]
            for ingredient in needed_list:
                query += f" AND Ingredients LIKE '%{ingredient}%'"

        if ingredients_not_needed:
            not_needed_list = [ingredient.strip() for ingredient in ingredients_not_needed.split(',')]
            for ingredient in not_needed_list:
                query += f" AND Ingredients NOT LIKE '%{ingredient}%'"

        # Retrive the query result
        conn = get_connection()
        try:
            results = pd.read_sql_query(query, conn)
            if not results.empty:
                st.write(results)
            else:
                st.write("No products found with the specified criteria.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    main()

