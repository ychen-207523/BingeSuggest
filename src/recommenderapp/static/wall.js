
const posts = [
    { username: 'User1', movie: 'Movie1', review: 4, comment: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', imdbID:'tt0086190' },
    { username: 'User2', movie: 'Movie1', review: 3.5, comment: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', imdbID:'tt0371746' },
    { username: 'User3', movie: 'Movie1', review: 2, comment:'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', imdbID:'tt0126029' },
    { username: 'User1', movie: 'Movie1', review: 4, comment: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', imdbID:'tt0415306' },
    { username: 'User2', movie: 'Movie1', review: 3.5, comment: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', imdbID:'tt0120484' },
    { username: 'User3', movie: 'Movie1', review: 2, comment:'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', imdbID:'tt0317219' },
  ];


  $(document).ready(function () {
    renderPosts();
  });

  var result = '';

  function fetchMovieData(imdbID){

    var apikey = '77da67f1';
    
    return new Promise(function(resolve, reject){

        $.ajax({
            type: 'GET',
            url: 'http://www.omdbapi.com/',
            dataType: 'json',
            data: {
                i: imdbID,
                apikey: apikey,
            },
            success: function(response) {
                resolve(response);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
  }

  async function renderPosts() {
    const postContainer = $('#post-container');

    posts.forEach(post => buildPost(post, postContainer));
  }

async function buildPost(post, postContainer){

    var postDiv = $('<div>').addClass('post');

    var imageDiv = $('<div>');
    var userDiv = $('<div>');
    
    var movieData;
    try{
        movieData = await fetchMovieData(post.imdbID);
    } catch(error){
        console.error(error);
    }
    
    var image = $('<img>', {src: movieData.Poster, alt: 'Image not found', style: 'width:100px;'})

    var titleDiv = $('<div>').addClass('postTitle');

    var usernameDiv = $('<div>').addClass('username').text(post.username);

    var postTitleText = $('<div>').addClass('postTitleText').text('reviewed');

    var movieNameDiv = $('<div>').addClass('moviename').text(movieData.Title);

    titleDiv.append(usernameDiv, postTitleText, movieNameDiv);

    var reviewDiv = $('<div>').addClass('review');

    for(let i = 0; i < post.review; i++){
        var star = $('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16"><path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/></svg>');
        reviewDiv.append(star);
    }

    var halfStar = $('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star-half" viewBox="0 0 16 16"><path d="M5.354 5.119 7.538.792A.516.516 0 0 1 8 .5c.183 0 .366.097.465.292l2.184 4.327 4.898.696A.537.537 0 0 1 16 6.32a.548.548 0 0 1-.17.445l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256a.52.52 0 0 1-.146.05c-.342.06-.668-.254-.6-.642l.83-4.73L.173 6.765a.55.55 0 0 1-.172-.403.58.58 0 0 1 .085-.302.513.513 0 0 1 .37-.245l4.898-.696zM8 12.027a.5.5 0 0 1 .232.056l3.686 1.894-.694-3.957a.565.565 0 0 1 .162-.505l2.907-2.77-4.052-.576a.525.525 0 0 1-.393-.288L8.001 2.223 8 2.226v9.8z"/></svg>');
    if((post.review * 10) % 10 > 0){
        reviewDiv.append(halfStar);
    }

    var commentDiv = $('<div>').addClass('comment').text(post.comment);

 
    var dataDiv = $('<div>').addClass('movie-data');

    var ratedDiv = $('<div>').text(movieData.Rated);
    var yearDiv = $('<div>').text(movieData.Year);
    var genreDiv = $('<div>').text(movieData.Genre);
    var runtimeDiv = $('<div>').text(movieData.Runtime);

    dataDiv.append(ratedDiv, yearDiv, genreDiv, runtimeDiv);

    imageDiv.append(image);
    userDiv.append(titleDiv, reviewDiv, commentDiv);
    postDiv.append(imageDiv, userDiv, dataDiv);
    postContainer.append(postDiv);
}