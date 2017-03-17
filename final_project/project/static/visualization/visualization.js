window.onload = function(e) {

  getAllData(null, function(data) {
    dataPoints = [];
    times = [];
    for(var i = 0; i < data.length; i++) {
      dataPoints.push(data[i].value);

      var date = new Date(data[i].time);

      var dateStr = "";
      if(date.getHours() > 12) {
        var dateStr =
          (date.getMonth() + 1) + "/" +
          date.getDay() + "/" +
          date.getFullYear() + " " +
          (date.getHours() > 12 ? date.getHours() - 12 : date.getHours()) + ":" +
          (date.getMinutes() < 9 ? "0" + date.getMinutes() : date.getMinutes()) +
          (date.getHours() > 12 ? "pm" : "am");
      }

      times.push(dateStr);
    }

    var myChart = new Chart($("#dataVisChart"), {
        type: 'line',
        data: {
            labels: times,
            datasets: [{
                label: 'Temperature',
                data: dataPoints
                /*
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1*/
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });

    function addData(time, value) {
      myChart.data.labels.push(time);
      myChart.data.datasets[0].data.push(value);
      myChart.update(100);
    }

    /*
    setInterval(function() {
      var date = new Date(Date.now());

      var dateStr = "";
      if(date.getHours() > 12) {
        var dateStr =
          (date.getMonth() + 1) + "/" +
          date.getDay() + "/" +
          date.getFullYear() + " " +
          (date.getHours() > 12 ? date.getHours() - 12 : date.getHours()) + ":" +
          (date.getMinutes() < 9 ? "0" + date.getMinutes() : date.getMinutes()) +
          (date.getHours() > 12 ? "pm" : "am");
      }

      addData(dateStr, Math.random() * 100);
    }, 1000);*/

  });
}

function addOption(name) {
  $("#options").append("<option>" + name + "</option>")
}
