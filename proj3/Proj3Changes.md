# Project 3 Changes
## User System
### Log-in Page
Users of the application are now greeted with a sign-in page, or may choose to continue as a guest. The guest functionality is limited, but users who are logged in experience a more personalized experience.

Details on these additions can be found here: [The Login Page](https://github.com/brwali/PopcornPicks/blob/master/docs/frontend.md#the-login-page)

### Saved Reviews
Users can rate their favorite (or least favorite) movies out of ten possible points, as well as write brief comments to document their thoughts.

Details on these additions can be found here: [Review Page](https://github.com/brwali/PopcornPicks/blob/master/docs/frontend.md#review-page)

### The Wall
Users can view all of their movie reviews and ratings at a glance in a visually appealing dashboard.

Details on these additions can be found here: [Wall](https://github.com/brwali/PopcornPicks/blob/master/docs/frontend.md#walljs)

### Friends
People are often interested in what their friends are watching. With the project 3 updates, this is now possible. As long as users are friends, they are able to see what they have reviewed.

Details on these additions can be found here: [Profile and Friends](https://github.com/brwali/PopcornPicks/blob/master/docs/frontend.md#the-profile-page)

### Relevant Suggestions
The core functionality of recommending movies is improved by letting users see their recently reviewed movies to make the experience more unique to each user.

Details on these additions can be found here: [Search Page](https://github.com/brwali/PopcornPicks/blob/master/docs/frontend.md#search-page)

### Database
#### Users Table
This table was required for storing user information including username, email, and encrypted password.
|idUsers|username|email|password|
|--|----|----|--------|
|.|.|.|.|

#### Ratings Table
This table was required for storing ratings made by users. Information such as userID, movieID, the rating out of ten, and some comments.
|idRatings|user_id|movie_id|score|review|time|
|--|--|--|--|------------|---|
|.|.|.|.|.|.|

#### Movies Table
This table was required for storing movie names, their ID, and IMDB handle.
|idMovies|name|imdb_id|
|--|---------|---|
|.|.|.|

#### Friends Table
This table was required for storing friend information between different users
|idFriendship|idUsers|idFriend|
|--|--|--|
|.|.|.|

## Documentation
