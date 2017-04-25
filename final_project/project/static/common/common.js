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
    url: "/api/data/?format=json",
    dataType: "json",
    username: username,
    password: password,
    success: whenDone
  });
}

/**
 * Gets all of the pages of data associated with a GET request. Upon every
 * page being recieved, calls "whenDone".
 * @param  {[type]} whenDone [description]
 * @return {[type]}          [description]
 */
function getAllData(onUpdate, onComplete) {
  getAllDataRecur("/api/?format=json", [], onUpdate, onComplete);
}

/**
 * Recursive call that gets all the pages of data. Don't call this directly,
 * instead use "getAllData".
 * @param  {String} nextURL  The url to call GET on
 * @param  {Array} dataAccumulater An array of elements collected so far
 * @param  {function} onUpdate A function called every time some more data is found
 * @param  {function} onComplete A function called when all data is found
 * @return {Array} An array of all the elements found
 */
function getAllDataRecur(nextURL, dataAccumulater, onUpdate, onComplete) {
  if(nextURL === null) {
    if(typeof onComplete === "function") {
      onComplete(dataAccumulater);
    }
  }

  getNextData(nextURL, function(data, success) {
    dataAccumulater = dataAccumulater.concat(data.results);
    if(typeof onUpdate === "function") {
      onUpdate(data, success);
    }
    getAllDataRecur(data.next, dataAccumulater, onUpdate, onComplete);
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
 * @param  {String} source_id ID of the source we're posting to
 * @param  {String} type   The category of the data
 * @param  {Integer} value  The value
 * @param  {String} time An ISO string representing the time uploaded
 * @param  {function} whenDone A callback function called when the post request finishes
 */
function createData(source_id, category, value, create_time, whenDone) {
  var dat = '{ "source_id": "' + source_id + '", "category": "' + category + '", "value": ' + value + ', "create_time": ' + create_time + ' }';
  console.log("Trying to post data: '" + dat + "'");

  $.ajax({
    type: "POST",
    url: "/api/data/?format=api",
    username: username,
    password: password,
    data: dat,
    contentType: "application/json",
    success: whenDone
  });
}

function updateData(data_id, category, value, whenDone) {
  //Update the time to represent the value (TODO: CHANGE THIS TO USE ORIGINAL)
  time = new Date(Date.now()).toISOString();

  url = "/api/data/" + data_id + "/";
  console.log("Put to url: '" + url + "'")

  //var dat = '{ "category": "' + type + '", "value": ' + value + ', "source": "' + source + '", "time": "' + time + '" }'
  var dat = '{ "category": "' + category + '", "value": ' + value + ' }'
  console.log("Data: '" + dat + "'")
  $.ajax({
    type: "PUT",
    url: url,
    username: username,
    password: password,
    data: dat,
    contentType: "application/json",
    success: whenDone
  })
}

function deleteData(key, whenDone) {
  $.ajax({
    type: "DELETE",
    url: "/api/data/" + key + "/",
    username: username,
    password: password,
    contentType: "application/json",
    success: whenDone
  })
}

function searchData(whenDone, source_id, minTime, maxTime) {
  var dataObject = {"source_id": source_id};
  if(minTime && maxTime) {
    dataObject.time_range = minTime + "-" + maxTime;
  }

  $.ajax({
    type: "POST",
    url: "/api/search/",
    username: username,
    password: password,
    data: JSON.stringify(dataObject),
    contentType: "application/json",
    success: whenDone
  })
}

////////////////////////////////////////////////////////////////////////////////
/* Source API */
////////////////////////////////////////////////////////////////////////////////

function createSource(name, whenDone) {
  var dat = '{  "source_name": "' + name + '" }';
  console.log("Trying to post data: '" + dat + "'")

  $.ajax({
    type: "POST",
    url: "/api/source/",
    username: username,
    password: password,
    data: dat,
    contentType: "application/json",
    success: whenDone
  });
}

function getSource(sourceID, whenDone) {
  $.ajax({
    type: "GET",
    url: "/api/source/" + sourceID + "/",
    username: username,
    password: password,
    contentType: "application/json",
    success: whenDone
  })
}

function getAllSources(whenDone) {
  $.ajax({
    type: "GET",
    url: "/api/source/",
    username: username,
    password: password,
    contentType: "application/json",
    success: whenDone
  })
}

function updateSource(sourceID, newName, whenDone) {
  var dat = '{ "source_name": "' + newName + '" }';
  console.log("Calling updateSource with data: '" + dat + "'");
  $.ajax({
    type: "PUT",
    url: "/api/source/" + sourceID + "/",
    username: username,
    password: password,
    data: dat,
    contentType: "application/json",
    success: whenDone
  })
}

function deleteSource(sourceID, whenDone) {
  $.ajax({
    type: "DELETE",
    url: "/api/source/" + sourceID + "/",
    username: username,
    password: password,
    contentType: "application/json",
    success: whenDone
  })
}

////////////////////////////////////////////////////////////////////////////////
/* Prediction API */
////////////////////////////////////////////////////////////////////////////////

function postLinear(source1, minTime1, maxTime1, source2, minTime2, maxTime2, k, whenDone) {
  //var dat = '{ "source_id1": "' + source1 + '", "min_time1": ' + minTime1 + ', "max_time1": ' + maxTime1 + ', "source_id2": "' + source2 + '", "min_time2": ' + minTime2 + ', "max_time2": ' + maxTime2 + ', "k": ' + k + '}';

  var dat = JSON.stringify({
    "source_id1": source1,
    "min_time1": minTime1,
    "max_time1": max_time1,
    "source_id2": source2,
    "min_time2": minTime2,
    "max_time2": maxTime2,
    "k": k
  })

  console.log("postLinear with data '" + dat + "'");
  $.ajax({
    type: "POST",
    url: "/api/predict/linear/",
    username: username,
    password: password,
    data: dat,
    contentType: "application/json",
    success: whenDone
  })
}

//

//createSource("Testing3", function(data, err) { console.log(data); console.log(err); });
//deleteSource("ad5d4493-7beb-47d5-b497-aebbc86106e2", function(data, err) { console.log(data); console.log(err); });
//getSource("Testing2");
