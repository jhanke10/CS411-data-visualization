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

// General stuff
function getMonth(mon){
   var d = Date.parse(mon + " 1, 2012");
   if(!isNaN(d)){
      return new Date(d).getMonth();
   }
   return -1;
 }

 function dateToMillis(date) {
 	var date_string = date.split(" ");
 	var time_string = date_string[3].split(":");
 	var d = new Date(parseInt(date_string[2]), getMonth(date_string[0]), parseInt(date_string[1]), parseInt(time_string[0]), parseInt(time_string[1]), parseInt(time_string[2]));
  console.log(parseInt(date_string[2]));
  console.log(getMonth(date_string[0]));
  console.log(parseInt(date_string[1]));
  console.log(parseInt(time_string[0]));
  console.log(parseInt(time_string[1]));
  console.log(parseInt(time_string[2]));
 	return d.getTime();
 }

 function millisToDate(millis) {
   date = new Date(0);
   date.setUTCMilliseconds(millis);
   var dateItself = date.toDateString();
   dateItself = dateItself.substring(dateItself.indexOf(" ") + 1);

   var hours = date.getHours();
   var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
   var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
   var timeItself = hours + ":" + minutes + ":" + seconds;

   return dateItself + " " + timeItself;
 }


////////////////////////////////////////////////////////////////////////////////
/* Data API */
////////////////////////////////////////////////////////////////////////////////

//Get specific data
function getData(data_id, whenDone) {
  $.ajax({
    type: "GET",
    url: "/api/data/" + data_id + "/",
    dataType: "json",
    username: username,
    password: password,
    success: whenDone
  });
}

function getDataBySource(source_id, whenDone) {
  var dat = JSON.stringify({"source_id": source_id});

  $.ajax({
    type: "POST",
    url: "/api/search/",
    username: username,
    password: password,
    data: dat,
    contentType: "application/json",
    success: whenDone
  })
}

/**
 * TODO: add parameters for specifying what data to get
 * Async function that wraps a get request
 * @param  {function} whenDone A callback function called when the get request finishes
 */
function getAllData(whenDone) {
  $.ajax({
    type: "GET",
    url: "/api/data/",
    dataType: "json",
    username: username,
    password: password,
    success: whenDone
  });
}

/**
 * Async function that wraps a post request
 * Note that "source_id" and "upload_time" can't be changed.
 * @param  {String}   source_id ID of the source we're posting to
 * @param  {String}   category   The category of the data
 * @param  {Integer}  value  The value
 * @param  {String}   create_time A long representing millis since epoch
 * @param  {function} whenDone A callback function called when the post request finishes
 */
function createData(source_id, category, value, create_time, whenDone) {
  var dat = JSON.stringify({
    "source_id": source_id,
    "category": category,
    "value": value,
    "create_time": create_time
  });

  console.log(dat);

  $.ajax({
    type: "POST",
    url: "/api/data/",
    username: username,
    password: password,
    data: dat,
    contentType: "application/json",
    success: whenDone
  });
}

function updateData(data_id, category, value, create_time, whenDone) {
  var dat = JSON.stringify({
    "data_id": data_id,
    "category": category,
    "value": value,
    "create_time": create_time
  })

  url = "/api/data/" + data_id + "/";
  console.log("Put to url: '" + url + "'")

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

function deleteData(data_id, whenDone) {
  $.ajax({
    type: "DELETE",
    url: "/api/data/" + data_id + "/",
    username: username,
    password: password,
    contentType: "application/json",
    success: whenDone
  })
}

function searchData(source_id, minTime, maxTime, whenDone) {
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

function postLinearData(x, y, k, whenDone) {
  var dat = JSON.stringify({
    "x": x,
    "y": y,
    "k": k
  });

  $.ajax({
    type: "POST",
    url: "/api/predict/linearData/",
    username: username,
    password: password,
    data: dat,
    contentType: "application/json",
    success: whenDone
  });
}

function postCompare(source1, source2, whenDone) {
  var dat = JSON.stringify({
    "s1": source1,
    "s2": source2
  });

  $.ajax({
    type: "POST",
    url: "/api/compare/",
    username: username,
    password: password,
    data: dat,
    contentType: "application/json",
    success: whenDone
  });
}

//

//createSource("Testing3", function(data, err) { console.log(data); console.log(err); });
//deleteSource("ad5d4493-7beb-47d5-b497-aebbc86106e2", function(data, err) { console.log(data); console.log(err); });
//getSource("Testing2");
