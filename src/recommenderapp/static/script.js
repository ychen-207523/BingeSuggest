$(document).ready(function () {

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
        var ulList = $("#selectedMovies");
        // Check if the value already exists in the list
        if (ulList.find('li:contains("' + ui.item.value + '")').length > 0) {
          $("#searchBox").val("");
          return false;
        }

        var li = $("<li class='list-group-item'/>")
          .text(ui.item.value)
          .appendTo(ulList);
        $("#searchBox").val("");
        return false;
      },

      // changed the min-length for searching movies from 2 to 1
      minLength: 1,
    });
  });

  $("#predict").click(function () {
    $("#loader").attr("class", "d-flex justify-content-center");

    var movie_list = [];

    $("#selectedMovies li").each(function () {
      movie_list.push($(this).text());
    });

    var movies = { movie_list: movie_list };

    // Clear the existing recommendations
    $("#predictedMovies").empty();

    // if movies list empty then throw an error box saying select atleast 1 movie!!
    if (movie_list.length == 0) {
      alert("Select atleast 1 movie!!");
    }

    $.ajax({
      type: "POST",
      url: "/predict",
      dataType: "json",
      contentType: "application/json;charset=UTF-8",
      traditional: "true",
      cache: false,
      data: JSON.stringify(movies),
      success: function (response) {
        var ulList = $("#predictedMovies");
        var i = 0;
        var recommendations = response["recommendations"];
        var imdbIds = response["imdb_id"]
        for (var i = 0; i < recommendations.length; i++) {
          var element = recommendations[i];
          var imdbID = imdbIds[i]
          var diventry = $("<div/>");
          var fieldset = $("<fieldset/>", { id: i }).css("border", "0");
          var link = $("<a/>").text("IMDb🔗").css({"text-decoration": "none"}).attr("href", "https://www.imdb.com/title/" + imdbID);
          var li = $("<li/>").text(element);
          var radios = $(`
                    <table class='table predictTable'>
                      <tr>
                        <td class='radio-inline'>
                          <section id="pattern1">
                            <label style="--icon:'😍"><input type="radio" name="${i}" value='3' data-toggle="tooltip" data-placement="top" title="LIKE"></label><br />
                          </section>
                        </td>
                        <td class='radio-inline'>
                          <section id="pattern1">
                            <label style="--icon:'😐'"><input type="radio" name="${i}" value='2' data-toggle="tooltip" data-placement="top" title="YET TO WATCH"></label><br />
                          </section>
                        </td>
                        <td class='radio-inline'>
                          <section id="pattern1">
                            <label style="--icon:'😤'"><input type="radio" name="${i}" value='1' data-toggle="tooltip" data-placement="top" title="DISLIKE"></label><br />
                          </section>
                        </td>
                      </tr>
                    </table>
                  `);

          diventry.append(li);
          diventry.append(link);
          diventry.append(radios);
          fieldset.append(diventry);
          ulList.append(fieldset);
        }

        $("#loader").attr("class", "d-none");
      },
      error: function (error) {
        console.log("ERROR ->" + error);
        $("#loader").attr("class", "d-none");
      },
    });
  });

  window.addEventListener("popstate", function (event) {
    // Check if the user is navigating back
    if (event.state && event.state.page === "redirect") {
      // Redirect the user to a specific URL
      window.location.href = "/";
      location.reload();
    }
  });

  // Function to handle Get Started button click
  function getStarted() {
    // Navigate to the search page
    $("#loaderLanding").attr("class", "d-flex justify-content-center");
    $("#centralDivLanding").hide();
    $('#landingTopNav').hide();
    setTimeout(function() {
      window.location.href = "/search_page"; // Replace with the actual URL of your search page
    }, 2000);
  }

  // Bind the getStarted function to the Get Started button click
  $("#getStartedButton").click(function () {
    getStarted();
  });

  var FeedbackData;

  $("#feedback").click(function () {
    notifyMeButton = document.getElementById("checkbox");
    notifyMeButton.disabled = false;
    var myForm = $("fieldset");
    var data = {};
    var labels = {
      1: "Dislike",
      2: "Yet to watch",
      3: "Like",
    };

    // to check if any movies selected before giving feedback
    if(myForm.length == 0){
      alert("No movies found. Please add movies to provide feedback.");
      return;
    }
    var error = false; // Flag to track errors

    for (var i = 0; i < myForm.length; i++) {
      var input = $("#" + i)
        .find("div")
        .find("input:checked")[0];
      var movieName = $("#" + i)
        .find("div")
        .find("li")[0].innerText;

      if (!input) {
        // If no selection is made, set error flag to true and break the loop
        error = true;
        break;
      }

      data[movieName] = labels[input.value];
    }

    if (error) {
      // Display an error message if there are missing selections
      alert("Please select a feedback for all movies.");
      return; // Exit the function without making the AJAX call
    }

    FeedbackData = data;
    localStorage.setItem("fbData", JSON.stringify(data));
    $.ajax({
      type: "POST",
      url: "/feedback",
      dataType: "json",
      contentType: "application/json;charset=UTF-8",
      traditional: "true",
      cache: false,
      data: JSON.stringify(data),
      success: function (response) {
        window.location.href = "/success";
      },
      error: function (error) {
        console.log("ERROR ->" + error);
      },
    });
  });

  $("#notifyButton").click(function () {
    var data = JSON.parse(localStorage.getItem("fbData"));
    $("#loaderSuccess").attr("class", "d-flex justify-content-center");
    if (!data) {
      alert("No feedback data found. Please provide feedback.");
      return;
    }
  
    var emailString = $("#emailField").val();
    data.email = emailString;
  
    // Remove the "emailSent" flag to allow sending the email again
    localStorage.removeItem("emailSent");
  
    $.ajax({
      type: "POST",
      url: "/sendMail",
      dataType: "json",
      contentType: "application/json;charset=UTF-8",
      traditional: "true",
      cache: false,
      data: JSON.stringify(data),
      success: function (response) {
        $("#loaderSuccess").attr("class", "d-none");
        $("#emailSentSuccess").show();
        setTimeout(function () {
          $("#emailSentSuccess").fadeOut("slow");
        }, 2000);
        $('#area1').attr('placeholder', 'Email'); 
        $('#emailField').val('');
      },
      error: function (error) {
        $("#loaderSuccess").attr("class", "d-none");
        console.log("ERROR ->" + error);
        localStorage.removeItem("fbData");
      },
    });
  });
  
});
