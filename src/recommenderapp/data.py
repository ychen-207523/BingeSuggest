import pandas as pd
import os
from imdb import IMDb
from concurrent.futures import ThreadPoolExecutor

# Initialize IMDb instance globally to reduce overhead
ia = IMDb()
i = 0

def get_imdb_rating_and_awards(imdb_id):
    global i
    i += 1
    print(i)
    if i % 10 == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        movie = ia.get_movie(imdb_id[2:])  # Removing 'tt' prefix
        rating = movie.get('rating', "No Rating Found")
        
        # Fetching awards if available
        awards = movie.get('awards', "No Awards Found")
        return rating, awards
    except Exception as e:
        print(f"Error fetching data for IMDb ID {imdb_id}: {e}")
        return "Error", "Error"

def update_csv_with_rating_and_awards(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Ensure 'imdb_id' column exists
    if 'imdb_id' not in df.columns:
        print("Error: 'imdb_id' column not found in the CSV file.")
        return

    # Check if 'rating' and 'awards' columns exist; if not, add them
    if 'rating' not in df.columns:
        df['rating'] = None
    if 'awards' not in df.columns:
        df['awards'] = None

    # Filter rows where rating or awards are still missing
    imdb_ids_to_fetch = df[(df['rating'].isnull()) | (df['awards'].isnull())]['imdb_id'].tolist()

    # Fetch rating and awards details concurrently for missing entries
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(get_imdb_rating_and_awards, imdb_ids_to_fetch))

    # Split the results into rating and awards columns
    ratings, awards = zip(*results)
    df.loc[df['rating'].isnull(), 'rating'] = ratings
    df.loc[df['awards'].isnull(), 'awards'] = awards

    # Save the updated DataFrame back to the CSV
    df.to_csv(file_path, index=False)
    print(f"Updated CSV saved with IMDb ratings and awards in '{file_path}'.")

# Usage example
csv_file_path = r'.\data\movies.csv'  # Replace with your file path
update_csv_with_rating_and_awards(csv_file_path)
