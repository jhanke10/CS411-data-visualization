//TODO: store this using environment variables
var username = "admin";
var password = "password123";

// We need to have cookie management stuff for post requests
var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
// End setup for cookie management

/**
 * TODO: add parameters for specifying what data to get
 * Async function that wraps a get request
 * @param  {function} whenDone A callback function called when the get request finishes
 */
function getData(whenDone) {
  $.ajax({
    type: "GET",
    url: "/api/?format=json",
    dataType: "json",
    username: username,
    password: password,
    /*
    success: function(data, status) {
      console.log("Finished get request. Response:");
      console.log(JSON.stringify(data));
      console.log(status);
      console.log("End get response.");
      return data;
    }*/
    success: whenDone
  });
}

/**
 * Gets all of the pages of data associated with a GET request. Upon every
 * page being recieved, calls "whenDone".
 * @param  {[type]} whenDone [description]
 * @return {[type]}          [description]
 */
function getAllData(whenDone) {
  getAllDataRecur("/api/?format=json", whenDone);
}

/**
 * Recursive call that gets all the pages of data. Don't call this directly,
 * instead use "getAllData".
 * @param  {[type]} nextURL  [description]
 * @param  {[type]} whenDone [description]
 * @return {[type]}          [description]
 */
function getAllDataRecur(nextURL, whenDone) {
  getNextData(nextURL, function(data, success) {
    whenDone(data, success);
    getAllDataRecur(data.next, whenDone);
  })
}

function getNextData(nextURL, whenDone) {
  console.log("GET request to " + nextURL);
  $.ajax({
    type: "GET",
    url: nextURL,
    dataType: "json",
    username: username,
    password: password,
    success: whenDone
  });
}

/**
 * Async function that wraps a post request
 * @param  {String} type   The category of the data
 * @param  {Integer} value  The value
 * @param  {String} source Where this data originated from
 * @param  {function} whenDone A callback function called when the post request finishes
 */
function postData(type, value, source, whenDone) {

  var dat = '{ "category": "' + type + '", "value": ' + value + ', "source": "' + source + '" }'
  console.log("Trying to post data: '" + dat + "'")

  $.ajax({
    type: "POST",
    url: "/api/?format=api",
    username: username,
    password: password,
    data: dat,
    contentType: "application/json",
    /*
    success: function(data, status) {
      console.log("Finished a post request. Response: ");
      console.log(JSON.stringify(data));
      console.log(status);
      console.log("End post response.");
      return data;
    }*/
    success: whenDone
  });
}
