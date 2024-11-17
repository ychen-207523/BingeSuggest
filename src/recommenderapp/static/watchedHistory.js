/**
 * Copyright (c) 2023 Nathan Kohen, Nicholas Foster, Brandon Walia, Robert Kenney
 * This code is licensed under MIT license (see LICENSE for details)
 *
 * @author: PopcornPicks
 */

// Fetch and render watched history when the page loads
$(document).ready(async function () {
    try {
        const watchedMovies = await loadWatchedHistory();
        renderWatchedHistory(watchedMovies);
    } catch (error) {
        console.error("Error loading watched history:", error);
    }
});

// Load watched history from the backend
function loadWatchedHistory() {
    return new Promise(function (resolve, reject) {
        $.ajax({
            type: "GET",
            url: "/getWatchedHistoryData",
            contentType: "application/json;charset=UTF-8",
            success: function (response) {
                console.log("Watched History Data:", response); // Debugging log
                resolve(response);
            },
            error: function (error) {
                reject(error);
            },
        });
    });
}

// Render watched history posts
async function renderWatchedHistory(watchedMovies) {
    const container = $("#watchedHistoryContainer");

    watchedMovies.forEach(async (movie) => {
        const movieDiv = $("<div>").addClass("movie-entry row mb-3 p-2 border-bottom");

        // Fetch metadata from OMDb API
        let movieData = {};
        try {
            movieData = await fetchMovieData(movie.imdb_id);
        } catch (error) {
            console.error("Error fetching movie data:", error);
        }

        // Movie Poster
        const posterDiv = $("<div>").addClass("col-md-2");
        const posterImg = $("<img>", {
            src: movieData.Poster || "placeholder.png",
            alt: "Poster not available",
            style: "width: 100%;",
        });
        posterDiv.append(posterImg);

        // Movie Details
        const detailsDiv = $("<div>").addClass("col-md-8");
        const title = $("<h5>").text(movieData.Title || movie.movie_name);
        const watchedOn = $("<p>").text(`Watched on: ${movie.watched_date}`);
        const genres = $("<p>").text(`Genres: ${movieData.Genre || "N/A"}`);
        detailsDiv.append(title, watchedOn, genres);

        // IMDb Link
        const imdbDiv = $("<div>").addClass("col-md-2 text-right");
        const imdbLink = $("<a>", {
            href: `https://www.imdb.com/title/${movie.imdb_id}`,
            target: "_blank",
            class: "btn btn-info btn-sm",
        }).text("IMDb");
        imdbDiv.append(imdbLink);

        // Append all components to the movie entry
        movieDiv.append(posterDiv, detailsDiv, imdbDiv);
        container.append(movieDiv);
    });
}

// Fetch movie metadata from OMDb API
function fetchMovieData(imdbID) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            type: "GET",
            url: "http://www.omdbapi.com/",
            dataType: "json",
            data: {
                i: imdbID,
                apikey: "77da67f1", // Replace with your OMDb API key
            },
            success: function (response) {
                resolve(response);
            },
            error: function (error) {
                reject(error);
            },
        });
    });
}
