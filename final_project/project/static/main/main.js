console.log("Main.js loaded");

/**
 * When the document loads, make sure to create the image slider.
 */
$(window).on('load', function() {
    $('#mainScrollImage').nivoSlider();
});

$("#username").on("blur", function() {
  console.log("Hi!");
  if($("#username").value().length() === 0) {
    $("#usernameLabel").css("color", "red");
    $("#usernameLabel").innerHTML = "Username: (this field is required!)";
  } else {
    $("#usernameLabel").css("color", "black");
    $("#usernameLabel").innerHTML = "Username:";
  }
})
