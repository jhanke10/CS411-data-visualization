
window.onload = function(e) {
  console.log("Added data via code!");
  $("#realtimeDataTable").append("<tr> <td>Foo</td> <td>2</td> <td>jQuery</td ></tr>");
  addData("Temperature", 89, "code");
}

function addData(type, value, source) {
  var html = "<tr> <td>" + type + "</td> <td>" + value + "</td> <td>" + source + "</td ></tr>"
  $("#realtimeDataTable").append(html);
}
