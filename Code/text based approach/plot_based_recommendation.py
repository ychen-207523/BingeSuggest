import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def get_data(movie_length):
    metadata = pd.read_csv("movies_metadata.csv", low_memory=False)
    return metadata[:movie_length]


def compute_tfidfmatrix(metadata):
    # Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words="english")

    # Replace NaN with an empty string
    metadata["overview"] = metadata["overview"].fillna("")

    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(metadata["overview"])

    cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)
    np.savez("cosine_similarity_10k", matrix=cosine_similarity)


def get_recommendations(title, indices, cosine_sim):
    # Get the index of the movie that matches the title

    if title not in indices:
        return None

    idx = indices[title]
    print("type")
    print(type(indices))
    print("indices")
    print(indices)
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return metadata["title"].iloc[movie_indices]


if __name__ == "__main__":
    metadata = get_data(movie_length=5000)

    # compute_tfidfmatrix(metadata)

    # Cosine similarity matrix is already saved.
    data = np.load("cosine_similarity_5k.npz", allow_pickle=True)
    cosine_similarity = data["matrix"]

    indices = pd.Series(metadata.index, index=metadata["title"]).drop_duplicates()
    play = True
    while play != False:
        movie = input("Name of movie from movie list: ")
        recommendations = get_recommendations(movie, indices, cosine_similarity)
        if recommendations is None:
            print("Given movie not in database, try again")
            continue

        print("Following are the recommended movies if you like : ", movie)
        print(recommendations)
        response = input("Do you want to continue?(yes/no)")
        if response == "no":
            play = False
