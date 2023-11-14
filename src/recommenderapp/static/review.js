$(document).ready(function () {

    var selectedMovie = ''; // Variable to store the selected movie
    
    $(function () {
        $("#searchBox").autocomplete({
        source: function (request, response) {
            $.ajax({
            type: "POST",
            url: "http://localhost:5000/search",
            dataType: "json",
            cache: false,
            data: {
                q: request.term,
            },
            success: function (data) {
                response(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(textStatus + " " + errorThrown);
            },
            });
        },
        select: function (event, ui) {
            // Clear the previous selection
            $("#selectedMovies").empty();
            selectedMovie = ui.item.value;
            // Append the new selection
            var li = $("<li class='list-group-item'/>").text(selectedMovie);
            $("#selectedMovies").append(li);
            $("#searchBox").val("");
            return false;
        },
        minLength: 1,
        });
    });

})