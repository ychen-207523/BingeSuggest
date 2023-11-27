_**Below we describe different test-case files that we have written for checking the working of PopcornPicks!**_

# [test_predict.py](https://github.com/brwali/PopcornPicks/blob/master/test/test_predict.py)

Here test cases are written to check if the recommendations made by PopcornPicks are of good quality. <br/>
For example, for a movie input of "Spider-Man (2002)" and rating 5.0, the recommender returns "Masters of the Universe (1987)", which is a fair recommendation.

# [test_search.py](https://github.com/brwali/PopcornPicks/blob/master/test/test_search.py)

Here test cases are written to check if the movie-searching feature of PopcornPicks returns similar outputs to the input string! <br/>
For example, for keyword "love" the top-10 searches that PopcornPicks returns consist of the word "Love" making it related to the input keyword.

# [test_util.py](https://github.com/brwali/PopcornPicks/blob/master/test/test_util.py)

Here test cases are written to check the functionality of the email notifier feature, i.e., for every function corresponding to the feature - test_beautify_feedback_data(), test_create_colored_tags(), test_create_movie_genres(), test_send_email_to_user(), test_accounts(), test_get_wall_posts(), test_get_username(), test_get_recent_movies(), test_friends() and test_submit_review()
