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
            //alert(data);
            // console.log(data);
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
        response["recommendations"].forEach((element) => {
          var diventry = $("<div/>");
          var fieldset = $("<fieldset/>", { id: i }).css("border", "0");
          var li = $("<li/>").text(element);
          var radios = $(`
                    <table class='table'>
                        <tr>
                        <td class='radio-inline'>
                            <label><input type='radio' name="${i}" value='1'>Dislike</label>
                        </td>
                        <td class='radio-inline'>
                            <label><input type='radio' name="${i}" value='2'>Yet to watch</label>
                        </td>
                        <td class='radio-inline'>
                            <label><input type='radio' name="${i}" value='3'>Like</label>
                        </td>
                        </tr>
                    </table>
                    `);

          diventry.append(li);
          diventry.append(radios);
          fieldset.append(diventry);
          ulList.append(fieldset);
          i += 1;
        });

        // var li = $('<li/>').text()
        console.log("->", response["recommendations"]);
      },
      error: function (error) {
        console.log("ERROR ->" + error);
      },
    });
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

    console.log(data);
    FeedbackData = data;
    localStorage.setItem("fbData", JSON.stringify(data));
    console.log(localStorage.getItem("fbData"));
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
        console.log("Success");
      },
      error: function (error) {
        console.log("ERROR ->" + error);
      },
    });
  });

  $("#notifyButton").click(function () {
    var data = JSON.parse(localStorage.getItem("fbData"));
  
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
        // localStorage.removeItem("fbData");
        $("#emailSentSuccess").show();
        // Hide the success message after 5 seconds (5000 milliseconds)
        setTimeout(function () {
          $("#emailSentSuccess").fadeOut("slow");
        }, 2000);
        console.log("Email sent successfully!")
        console.log(response);
      },
      error: function (error) {
        console.log("ERROR ->" + error);
        localStorage.removeItem("fbData");
      },
    });
  });
  
});
