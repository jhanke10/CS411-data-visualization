window.onload = function(e) {

  $("#importForm").hide();
  $("#insertForm").hide();
  $("#searchForm").hide();

  /*
  getAllData(function(data) {
    for(var i = 0; i < data.results.length; i++) {
      addDataRow(data.results[i].category, data.results[i].value, data.results[i].source, data.results[i].time);
    }
  });*/

  getData(function(data) {
    for(var i = 0; i < data.length; i++) {
      console.log("Data: " + data[i].dataID + ", " + data[i].name + ", " + data[i].value + ", " + data[i].time)
      addDataRow(data[i].name, data[i].value, data[i].time, data[i].dataID);
    }
  })

  $("#searchFor").on("input", function(event) {
    filterEntries($("#searchFor").val());
  })
}

function submitInsertForm() {
  var name = $("#insertName").val();
  var value = $("#insertValue").val();

  function setFail(nam, to) {
    to ? $(nam).attr("style", "border: 1px solid darkred") : $(nam).removeAttr("style");
    return to;
  }

  var failed =
    setFail("insertValue", value === "" || isNaN(value)) ||
    setFail("insertName", name === "");

  console.log("Failed?: " + failed);

  if(!failed) {
    $("#insertValue").val("");
    $("#insertName").val("");

    postData(name, value, function(data, success) {
      addDataRow(name, value, time);
    })
  }
}

function addDataRow(name, value, time, prepend=true) {

  parsedTime = time;//new Date(Date.parse(time));//new Date(Date.parse(time)).toTimeString();

  var html = $("<tr> <td>" + name + "</td> <td>" + value + "</td> <td>" + parsedTime + "</td> </tr>")
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
      event.preventDefault(); return false;
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
            $(entries[i]).parent().replaceWith('<td>' + vl + '</td>');

            data.push(vl);
          }

          //TODO: CALL PUT() request

          //console.log(new Date(Date.parse(ref.find("td")[3].innerHTML)));
          console.log(ref.find("td")[3].innerHTML);

          putData(ref.find("td")[3].innerHTML, data[0], data[1], data[2], function(data, success) {
            console.log("Put data with result: " + JSON.stringify(data));
            console.log("Success value: " + success);
          })

          $(document).off("click");
          ref.removeClass("editing");
        }
      });

      var entries = ref.find("td");
      for(let i = 0; i < entries.length - 1; i++) {
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
      deleteData($(this).find("td")[3].val(), function(data, success) {
        console.log("delete returned data: " + JSON.stringify(data));
        console.log("delete returned success code: " + success);
        $(this).hide();
      });;
    }
  });
}
