import pandas as pd
import warnings
import os

app_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.dirname(app_dir)
project_dir = os.path.dirname(code_dir)

warnings.filterwarnings("ignore")


def recommendForNewUser(user_rating):
    ratings = pd.read_csv(project_dir + "/data/ratings.csv")
    movies = pd.read_csv(project_dir + "/data/movies.csv")
    user = pd.DataFrame(user_rating)
    userMovieID = movies[movies["title"].isin(user["title"])]
    userRatings = pd.merge(userMovieID, user)

    moviesGenreFilled = movies.copy(deep=True)
    copyOfMovies = movies.copy(deep=True)
    for index, row in copyOfMovies.iterrows():
        copyOfMovies.at[index, "genres"] = row["genres"].split("|")
    for index, row in copyOfMovies.iterrows():
        for genre in row["genres"]:
            moviesGenreFilled.at[index, genre] = 1
    moviesGenreFilled = moviesGenreFilled.fillna(0)

    userGenre = moviesGenreFilled[moviesGenreFilled.movieId.isin(userRatings.movieId)]
    userGenre.drop(["movieId", "title", "genres"], axis=1, inplace=True)
    userProfile = userGenre.T.dot(userRatings.rating.to_numpy())
    moviesGenreFilled.set_index(moviesGenreFilled.movieId)
    moviesGenreFilled.drop(["movieId", "title", "genres"], axis=1, inplace=True)

    recommendations = (moviesGenreFilled.dot(userProfile)) / userProfile.sum()
    joinMoviesAndRecommendations = movies.copy(deep=True)
    joinMoviesAndRecommendations["recommended"] = recommendations
    joinMoviesAndRecommendations.sort_values(
        by="recommended", ascending=False, inplace=True
    )
    return [x for x in joinMoviesAndRecommendations["title"]][:201]
