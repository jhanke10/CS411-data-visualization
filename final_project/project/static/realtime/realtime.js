window.onload = function(e) {

  $("#importForm").hide();
  $("#insertForm").hide();

  getAllData(function(data) {
    for(var i = 0; i < data.results.length; i++) {
      addDataRow(data.results[i].category, data.results[i].value, data.results[i].source, false);
    }
  });
}

function submitInsertForm() {
  var type = $("#insertType").val();
  var value = $("#insertValue").val();
  var source = $("#insertSource").val();

  var failed = false;

  if(type === "") {
    $("#insertType").attr("style", "border: 1px solid darkred");
    failed = true;
  } else {
    $("#insertType").removeAttr("style");
  }

  if(value === "" || isNaN(value)) {
    $("#insertValue").attr("style", "border: 1px solid darkred");
    failed = true;
  } else {
    $("#insertValue").removeAttr("style");
    value = parseInt(value);
  }

  if(source === "") {
    $("#insertSource").attr("style", "border: 1px solid darkred; border-right: 2px solid darkred;");
    failed = true;
  } else {
    $("#insertSource").removeAttr("style");
  }

  if(!failed) {
    $("#insertType").val("");
    $("#insertValue").val("");
    $("#insertSource").val("");

    postData(type, value, source, function(data, success) {
      addDataRow(type, value, source);
    })
  }
}

function addDataRow(type, value, source, prepend=true) {
  var html = $("<tr> <td>" + type + "</td> <td>" + value + "</td> <td>" + source + "</td ></tr>")
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
          for(let i = 0; i < entries.length; i++) {
            var vl = $(entries[i]).val();
            if(vl === "") vl = $(entries[i]).attr("placeholder");
            $(entries[i]).parent().replaceWith('<td>' + vl + '</td>');
            //TODO: CALL PUT() request
          }
          $(document).off("click");
          ref.removeClass("editing");
        }
      });

      var entries = ref.find("td");
      for(let i = 0; i < entries.length; i++) {
        var vl = entries[i].innerHTML;
        $(entries[i]).replaceWith('<td><input type="text" placeholder="' + vl + '"></td>');
      }
    });

  if(prepend) {
    $("#realtimeDataTable").prepend(html);
  } else {
    $("#realtimeDataTable").append(html);
  }
}
