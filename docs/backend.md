# Functions Description of the backend

## [app.py](https://github.com/brwali/PopcornPicks/blob/master/src/recommenderapp/app.py)

### landing_page()
**Renders to the landing page of the web-app**

### search_page()
**Render to the search page of the web-app**

### predict()
**Returns movie recommendations on the basis of user-input movies**

### search()
**Returns top-10 movie searches for an input string in the search box**

### feedback()
**Handles user feedback submission**

### send_mail()
**Handles user feedback submission and mails the results**

### success()
**Renders to the success page**

## [utils.py](https://github.com/brwali/PopcornPicks/blob/master/src/recommenderapp/utils.py)

### create_colored_tags(genres)
**Utility function to create colored tags for different movie genres**<br/>
**Input: Movie genres;<br/> Output: Colored tags for those genres**

### beautify_feedback_data(data)
**Utility function to beautify the feedback json containing predicted movies for sending in email**<br/>
**Input: Data obtained from frontend in json format;<br/> Output: Beautified data dictionary containing movies grouped by watchlist category**

### create_movie_genres(movie_genre_df)
**Utility function for creating a dictionary for movie-genres mapping**<br/>
**Input: Data frame of movies.csv;<br/> Output: Dictionary of movies-genres mapping**

### send_email_to_user(recipient_email, categorized_data)
**Utility function to send movie recommendations to user over email**<br/>
**Input : email of recipient_email and output of [beautify_feedback_data](https://github.com/adipai/PopcornPicks/wiki/Backend/_edit#beautify_feedback_datadata);<br/> Output: Sends email for valid email, otherwise raises exception in the server logs**<br/>


## [search.py](https://github.com/brwali/PopcornPicks/blob/master/src/recommenderapp/search.py)
**Class that handles the search feature of the landing page.**

### starts_with(word)
**Function to check movie prefix**<br/>
**Input : word/initial character(s);<br/> Output : List of movies having that prefix**<br/>

### anywhere(word, visited_words)
**Function to check visited words**<br/>
**Input : Word and visited words;<br/> Output : Words that have not been visited**<br/>

### results(word)
**Function to serve the result render**
**Input : A word/initial character(s);<br/> Output : All titles starting with the given prompt.**<br/>

### results_top_ten(word)
**Function to get top 10 results**
**Input : A word/initial character(s);<br/> Output : Top 10 titles starting with the given prompt (taken from [results](https://github.com/adipai/PopcornPicks/wiki/Backend/_edit#resultsself-word))**<br/>

## Item_based.py
**Recommends movies to a user based on their past preferences and the preferences of users with similar tastes. Item-Item Collaborative Filtering (CF) is used to recommend similar movies based on user input. For example, if Joseph enjoyed Seven and Shutter Island, PopcornPicks might suggest The Prestige and Inception.**

### recommend_for_new_user(user_rating)
**Generates a list of recommended movie titles for a new user based on their selections via item-item based CF.**

