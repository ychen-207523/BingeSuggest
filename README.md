# <i>Movie Recommendation</i>
        A collaborative filtering based recommnedation enginer!


[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/ssp4all/)



[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/jayjagtap/Autofill-Buddy/graphs/commit-activity) [![Contributors Activity](https://img.shields.io/github/commit-activity/m/jayjagtap/Autofill-Buddy)](https://github.com/git-ankit/MovieRecommender/pulse) [![GitHub issues](https://img.shields.io/github/issues/jayjagtap/Autofill-Buddy.svg)](https://github.com/git-ankit/MovieRecommender/issues/) [![GitHub issues-closed](https://img.shields.io/github/issues-closed/jayjagtap/Autofill-Buddy.svg)](https://github.com/git-ankit/MovieRecommender/issues?q=is%3Aissue+is%3Aclosed) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4127507.svg)](https://doi.org/10.5281/zenodo.4127507) [![Build Status](https://travis-ci.com/git-ankit/MovieRecommender.svg?branch=master)](https://travis-ci.com/git-ankit/MovieRecommender) [![codecov](https://codecov.io/gh/git-ankit/MovieRecommender/branch/master/graph/badge.svg?token=8K0VL8106C)](undefined)

#### Setup ⚙️

#### Video ▶️ 

<a  href="https://youtu.be/OSjpryqI1RQ"><img height=150 width=500 alt="logo here" src="https://raw.githubusercontent.com/git-ankit/MovieRecommender/master/asset/video.png"/></a>

#### Working 👨‍💻

#### Documentation 📱
Recommend a user with a set of movies that they might like by considering the movies they have liked in the past and also considering the movies liked by other users that have a similar taste like them.</br>
</br>
Approaches:</br>
Content-Based</br>
Collaborative Filtering</br>
Item - Item Collaborative Filtering</br>
User - user Collaborative Filtering</br>

Our Approach</br>
There are two major approaches to implement recommendation systems: Content-Based and Collaborative Filtering.</br>
In Content-Based, we only consider the users’ past history and recommend movies from the genres that they have liked in the past.</br> 
In this project, we have implemented Collaborative Filtering (CF). Collaborative filtering has two types: Item-Item CF and User-User CF.</br> 
In Item-Item CF, we recommend the items that are most similar to the items liked by the user. Whereas, in User-User CF, we recommend the items liked by the users that are similar to the user we want to make a recommendation for.</br>

Important Functions in the code :</br>
recommend(userID): This function takes userID as the input and correlates it with different items in the case of Item-Item Collaborative Filtering and correlates with different users in User-User Collaborative Filtering to provide the best movies possible for the given user ID.</br>


Use Cases :</br>
</br>
Based on the Genre(Content Based) :</br>
Let’s consider Lisa’s favourite genre is Horror and she has watched Annabelle and The Conjuring.</br>
So, now Lisa would be getting suggestions IT, Us and Get Out which are of  same Genre.</br>

</br>
Based on the movies liked( Item - Item Collaborative Filtering) :</br>
Let’s consider Romeo has watched Seven and Shutter Island and he has rated both the movies 5/5.</br>
The Movie Database consists :</br>
Seven - 5/5</br>
Shutter Island - 5/5</br>
The Prestige - 5/5</br>
Inception - 5/5</br>
Hitman - ⅖</br>
So, according to the movie recommendation system, it uses Collaborative Filtering to get the movies from the database to get the movies which have a good rating and have been rated by a good number of users and then gives the suggestion to Romeo with the movies :</br>
The Prestige, Inception.</br>
</br>

Based on watch history ( User - User Collaborative Filtering ) :</br>
Let’s consider Romeo has watched Avenger’s Infinity War and has given a rating of 5.</br>
Now, let’s consider Juliet has watched movies Avenger’s Infinity War and Avenger’s Endgame and has rated both the movies very well (5/5).</br>
Now, according to the movie recommendation system, it uses Collaborative Filtering to get the movies from the other movies from different user’s with highest correlation and good rating and gives the suggestion to Romeo to watch Avenger’s Endgame.</br>
</br>
Join Us In Phase -2 to build Moviebuddy that would in-turn help us during this Pandemic. Cheers!</br>

