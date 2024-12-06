!pip install praw
!pip install pandas
!pip install textblob
!pip install openpyxl

import praw
import pandas as pd
from textblob import TextBlob
import re
import time

reddit = praw.Reddit(
    client_id='nqOA9ZwDX_wG6AkBp2G7EA',
    client_secret='VkNeO7D5CVJP5lYJ0xCXWzrGMQ_f0w',
    user_agent='Pet Food Research Script by /u/fayeshar2001',
    username='fayeshar2001',
    password='xiafei20011123'
)
# Load cleaned pet food brand data
cleaned_pet_food_df = pd.read_excel('Cleaned_OpenPetFoodFacts_PetFood.xlsx')

# Extract brand and product names to create a search pattern
brands_products = cleaned_pet_food_df['name'].dropna().unique().tolist() + cleaned_pet_food_df['product_id'].dropna().astype(str).unique().tolist()
search_pattern = '|'.join([re.escape(brand) for brand in brands_products])

# Select the subreddit to scrape
subreddit = reddit.subreddit('dogfood')

# Fetch 500 posts related to Dog Food
posts_data = []
for submission in subreddit.top(limit=200):  # Fetch top 500 posts
    submission.comments.replace_more(limit=0)  # Replace "more" comments
    sentiment = TextBlob(submission.selftext).sentiment.polarity if submission.selftext else 0
    matched_brands_products = ', '.join(re.findall(search_pattern, submission.selftext + ' ' + submission.title, re.IGNORECASE))
    posts_data.append({
        'Post_Title': submission.title,
        'Post_Author': submission.author.name if submission.author else 'Deleted',
        'Post_Body': submission.selftext,
        'Post_Score': submission.score,
        'Sentiment_Score': sentiment,
        'Matched_Brands_Products': matched_brands_products
    })
print("Starting to fetch comments...")
comments_data = []
for submission in subreddit.top(limit=200):  # Fetch top 50 posts to extract comments from
    time.sleep(1)  # Adding delay to avoid hitting rate limits
    submission.comments.replace_more(limit=2)  # Load a limited number of more comments
    for comment in submission.comments.list():
        # Check if comment contains any brand or product name
        if re.search(search_pattern, comment.body, re.IGNORECASE):
            sentiment = TextBlob(comment.body).sentiment.polarity
            matched_brands_products = ', '.join(re.findall(search_pattern, comment.body, re.IGNORECASE))
            comments_data.append({
                'Post_Title': submission.title,
                'Comment_Author': comment.author.name if comment.author else 'Deleted',
                'Comment_Body': comment.body,
                'Comment_Score': comment.score,
                'Sentiment_Score': sentiment,
                'Matched_Brands_Products': matched_brands_products
            })
# Convert the list of posts and comments to DataFrames
posts_df = pd.DataFrame(posts_data)
comments_df = pd.DataFrame(comments_data)

# Clean the posts and comments by removing rows with deleted authors and empty content
cleaned_posts_df = posts_df[(posts_df['Post_Author'] != 'Deleted') & (posts_df['Post_Body'].str.strip() != '')]
cleaned_comments_df = comments_df[(comments_df['Comment_Author'] != 'Deleted') & (comments_df['Comment_Body'].str.strip() != '')]

# Save both original and cleaned data to the same Excel file, with four sheets
with pd.ExcelWriter('reddit_pet_food_analysis.xlsx') as writer:
    posts_df.to_excel(writer, sheet_name='Raw_Posts', index=False)
    cleaned_posts_df.to_excel(writer, sheet_name='Cleaned_Posts', index=False)
    comments_df.to_excel(writer, sheet_name='Raw_Comments', index=False)
    cleaned_comments_df.to_excel(writer, sheet_name='Cleaned_Comments', index=False)

print("Data has been saved to 'reddit_pet_food_analysis.xlsx'")