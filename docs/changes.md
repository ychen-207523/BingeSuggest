# The Delta

This page is a brief summary of all the significant updates that we made from the old version [here](https://github.com/git-ankit/MovieRecommender).

## Brand New User-interface 

We now have a sleek and more appealing user interface and experience, newly branded as 'PopcornPicks'. The process to use the web application is very intuitive and simple for any user who wants to get some movie recommendations based on their previously liked movies, create a watchlist, and have it emailed to themselves or their friends.

**Older version :**

<img src="https://github.com/brwali/PopcornPicks/blob/master/asset/demo.gif" width="700" height="400">


**Latest version :**

<img src="https://github.com/brwali/PopcornPicks/blob/master/asset/demo_final.gif" width="700" height="400">

## Email Feature

So you have a bunch of movie recommendations from our recommender system. What do you do with it? Tell us your email and we'll have it emailed to you with some beautiful font and its genre tags.

**An snapshot of the email :**

![email.png](https://github.com/brwali/PopcornPicks/blob/master/asset/email.png)

## Updated Database

We added new information corresponding to each movie in the database like IMDB ID, movie overview, poster path, and total runtime that has been obtained from the [Official GroupLens Website](https://grouplens.org/datasets/movielens/latest/). For further releases, we plan to use the additional information, pulling it up on the website while showing the list of recommended movies.

## Fixed Bugs

Some bugs we found in the initial version and the updates/solutions :
1. Two characters are required for movie search to trigger auto-complete
The movie search feature took 2 characters to give auto-complete options. This can be fairly ambiguous for the user, particularly making them feel that the application isn't working.

      *Solution: Type a character and you have auto-complete options. The more characters you type, it changes accordingly.*

2. Open-ended stuff or edge cases?
How do you know what to do? What if you don't select enough movies? What if you don't give all the feedback required to make a watchlist? What if you don't tell us the names of your liked movies (no input altogether)?

      *Solution: We have popups that deal with these edge cases and guide the user to follow the expected flow of control to have the best user experience with the web application.*

3. Repetitive occurrence of selected movies in movie search
Movies once chosen in the search showed up in the search auto-complete, available to be chosen again. This leads to splicing and key errors in the server logs.

      *Solution: Users can choose a movie only once in the movie search (even if you like the movie so much 😆). The recommender system gets a unique list of inputs to do it's magic*

4. No refresh on predict
All buttons were open to be used irrespective of the current state of the web application. This confuses the user, in that, gets them undecided on what to do next on the UI.

      *Solution: Have a deterministic user experience by guiding them to use the features as expected by the backend for a seamless experience. We use popups on the frontend and code updates in the backend to render a seamless experience.*

## Test Suite 
We now have an automated test suite(test_predict.py, test_search.py, test_util.py) that runs every time code commits are made into the master branch, with a code coverage report. The test suite workflow runs can be seen [here](https://github.com/brwali/PopcornPicks/actions/workflows/unittest.yml) and code coverage analysis [here](https://github.com/brwali/PopcornPicks/actions/workflows/codecoverage.yml).

**A snapshot of the test suite-workflows being run every time we commit!**
<img src="https://github.com/brwali/PopcornPicks/blob/master/asset/workflows.gif" width="700" height="300">

## Modularised Code
A small overhaul of the codebase to make it more modular for improving compatibility with proper doc-strings, unit testing, and increasing code coverage and scalability.

## Coding Standards
We believe that well-documented, modular, and clean code makes everyone's life easier. We have incorporated automated Pylint checks to make sure that every commit conforms to PEP8 Python standards. We try our best to have a score of 10.00 to make sure our code is easy to work with (but with increasing codebase size, you could probably decide on a smaller threshold < 10.00). You can find workflow runs [here](https://github.com/brwali/PopcornPicks/actions/workflows/pylint.yml).

![Spaces and tabs](https://github.com/brwali/PopcornPicks/blob/master/asset/space_tab_gif.gif)






