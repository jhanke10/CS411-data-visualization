window.onload = function(e) {

  $("#importForm").hide();
  $("#insertForm").hide();
  $("#searchForm").hide();

  $("#insertSourceForm").hide();
  $("#updateSourceForm").hide();

  /*
  getAllData(function(data) {
    for(var i = 0; i < data.results.length; i++) {
      addDataRow(data.results[i].category, data.results[i].value, data.results[i].source, data.results[i].time);
    }
  });
  */


  getAllSources(function(data) {
    //console.log(JSON.stringify(data));
    for(var i = 0; i < data.length; i++) {
      addSourceRow(data[i].source_id, data[i].source_name);
    }

    //Set up default insert form text
    var source_id = $("#sourceDropdown").val();
    //console.log(source_id);
    source_id = source_id.substring(source_id.indexOf("=") + 1, source_id.indexOf(")"));

    var name = $("#sourceDropdown").val();
    name = name.substring(0, name.indexOf(" "));
    $("#insertSource").val("Source: " + name);
    $("#insertSource").attr("sourceID", source_id);

    getDataBySource(source_id, function(data) {
      //console.log("Returned data: " + JSON.stringify(data));
      for(var i = 0; i < data.results.length; i++) {
        addDataRow(data.results[i].data_id, data.results[i].category, data.results[i].value, data.results[i].create_time, data.results[i].upload_time);
      }
    });
  });

  $("#searchFor").on("input", function(event) {
    filterEntries($("#searchFor").val());
  })
}

function submitInsertForm() {
  var source = $("#insertSource").attr("sourceid");
  var category = $("#insertCategory").val();
  var value = $("#insertValue").val();
  var create_time = $("#insertTime").val();

  function setFail(name, to) {
    to ? $(name).attr("style", "border: 1px solid darkred") : $(name).removeAttr("style");
    return to;
  }

  var failed =
    setFail("insertSource", source === "") ||
    setFail("insertType", category === "") ||
    setFail("insertValue", value === "" || isNaN(value)) ||
    setFail("insertTime", create_time !== "" && isNaN(time));

  if(!failed) {
    if(create_time === "") {
      create_time = new Date(Date.now()).getTime();
    }

    $("#insertCategory").val("");
    $("#insertValue").val("");
    $("#insertTime").val("");

    //createData(source_id, category, value, create_time, whenDone)
    //console.log(source);
    createData(source, category, value, create_time, function(data, success) {
      //console.log(JSON.stringify(data));
      addDataRow(data.data_id, category, value, create_time, data.upload_time);
    })
  }
}

//function addDataRow(type, value, source, time, prepend=true) {
function addDataRow(id, category, value, createTime, uploadTime, prepend=true) {

  parsedCreateTime = millisToDate(createTime);
  parsedUploadTime = millisToDate(uploadTime);

  //var html = $("<tr> <td>" + type + "</td> <td>" + value + "</td> <td>" + source + "</td> <td>" + parsedTime + "</td> </tr>")
  var html = $("<tr> <td>" + id + "</td> <td>" + category + "</td> <td>" + value + "</td> <td>" + parsedCreateTime + "</td> <td>" + parsedUploadTime + "</td> </tr>")
    .on("click", function(event) {
      var row = $(this);

      if ((event.ctrlKey || event.metaKey) || event.shiftKey) {
        row.addClass("highlight");
      } else {
        $("#realtimeDataTable tr").removeClass("highlight");
        row.addClass("highlight");
      }
    })
    .on("selectstart dragstart", function(event) {
      //event.preventDefault(); return false;
    })
    .on("dblclick", function(event) {
      var ref = $(this);

      if(ref.hasClass("editing")) {
        return false;
      } else {
        ref.addClass("editing");
      }

      $(document).on("click", function(event) {

        if(!$.contains(ref[0], event.target)) {
          var entries = ref.find("td input");

          var data = [];

          for(let i = 0; i < entries.length; i++) {
            var vl = $(entries[i]).val();
            if(vl === "") vl = $(entries[i]).attr("placeholder");

            if(i === entries.length - 1) {
              var reg = /\D/;
              if(reg.test(vl)) {
                console.log("Value before: " + vl);
                vl = dateToMillis(vl);
                console.log("Value after: " + vl);
              }
            }

            data.push(vl);

            if(i === entries.length - 1) {
              console.log("Value before: " + vl);
              vl = millisToDate(parseInt(vl));
              console.log("Value after: " + vl);
            }

            $(entries[i]).parent().replaceWith('<td>' + vl + '</td>');
          }

          //TODO: CALL PUT() request

          //console.log(new Date(Date.parse(ref.find("td")[3].innerHTML)));
          //console.log(ref.find("td")[3].innerHTML);
          console.log(ref.find("td")[0].innerHTML);

          /*
          putData(ref.find("td")[3].innerHTML, data[0], data[1], data[2], function(data, success) {
            console.log("Put data with result: " + JSON.stringify(data));
            console.log("Success value: " + success);
          })
          */

          console.log(data[0]);

          //updateData(data_id, category, value, create_time, whenDone)
          updateData(ref.find("td")[0].innerHTML, data[0], data[1], data[2], function(data, success) {
            console.log("Put data with result: " + JSON.stringify(data));
            console.log("Success value: " + success);

          });

          $(document).off("click");
          ref.removeClass("editing");
        }
      });

      var entries = ref.find("td");
      for(let i = 1; i < entries.length - 1; i++) {
        var vl = entries[i].innerHTML;
        $(entries[i]).replaceWith('<td><input type="text" placeholder="' + vl + '"></td>');
      }
    });

    //Delete button with each row:
    //Set position of <tr> to relative first, then add
    //<button type="button" class="btn btn-danger" style="position: absolute; height: calc(100% - 4px); margin: 2px; right: 0px;">X</button>

  if(prepend) {
    $("#realtimeDataTable").prepend(html);
  } else {
    $("#realtimeDataTable").append(html);
  }
}

function clearData() {
  $("#realtimeDataTable").empty();
}

function filterEntries(search) {
  search = search.toLowerCase();
  var allRows = $("#realtimeDataTable tr");
  allRows.each(function(index, val) {
    $(this).hide();
    if($(this).html().toLowerCase().includes(search)) {
      $(this).show();
    }
  });
}

function deleteSelected() {
  var allRows = $("#realtimeDataTable tr");
  allRows.each(function(index, val) {
    if($(this).hasClass("highlight")) {
      var ref = this;
      deleteData($(this).find("td")[0].innerHTML, function(data, success) {
        console.log("delete returned data: " + JSON.stringify(data));
        console.log("delete returned success code: " + success);
        console.log($(this))
        $(ref).remove();
      });
    }
  });
}

function addSourceRow(id, name) {
  var newOption = document.createElement("option");
  newOption.innerHTML = name + " (id=" + id + ")";
  newOption.onclick = function() {
    $("#insertSource").val("Source: " + name);
    $("#insertSource").attr("sourceID", id);

    clearData();
    getDataBySource(id, function(data) {
      for(var i = 0; i < data.results.length; i++) {
        addDataRow(data.results[i].data_id, data.results[i].category, data.results[i].value, data.results[i].create_time, data.results[i].upload_time);
      }
    });
  }

  $("#sourceDropdown").append(newOption);
}

function copySourceIDToClipboard() {
  var text = $("#sourceDropdown").val();
  text = text.substring(text.indexOf("=") + 1, text.indexOf(")"));

  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val(text).select();
  document.execCommand("copy");
  $temp.remove();
}

function submitInsertSourceForm() {
    var source_name = $("#insertSourceField").val();

    function setFail(name, to) {
      to ? $(name).attr("style", "border: 1px solid darkred") : $(name).removeAttr("style");
      return to;
    }

    var failed = setFail("insertSourceField", source_name === "")

    if(!failed) {
      $("#insertSourceField").val("");

      createSource(source_name, function(data, success) {
        addSourceRow(data.source_id, data.source_name);
      })
    }
}

function submitUpdateSourceForm() {
  //TODO: PUT request to source
}
