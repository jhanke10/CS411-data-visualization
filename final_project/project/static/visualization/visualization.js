xData = [];
xSource = null;
yData = [];

myChart = null;

window.onload = function(e) {

  setInterval(function() {
    getDataBySource(xSource, function(dat) {
      xData = [];
      yData = [];
      for(let i = 0; i < dat.results.length; i++) {
        xData.push(dat.results[i].upload_time);
        yData.push(dat.results[i].value);
      }

      updateChart();

    })
  }, 200);

  getAllSources(function(data) {
    //console.log(JSON.stringify(data));

    if(data.length > 0) {
      xSource = data[0].source_id;
      getDataBySource(xSource, function(dat) {
        for(let i = 0; i < dat.results.length; i++) {
          xData.push(dat.results[i].upload_time);
          yData.push(dat.results[i].value);
        }
        console.log("X data: " + xData);
        console.log("Y data: " + yData);

        var mergedData = [];
        for(let i = 0; i < xData.length; i++) {
          mergedData.push({"x": xData[i], "y": yData[i]});
        }

        myChart = new Chart($("#dataVisChart"), {
            type: 'line',
            data: {
                label: "WIP",
                datasets: [
                  {
                    label: 'Testing!',
                    data: mergedData
                  }
                ]
            },
            options: {
                scales: {
                    xAxes: [{
                      type: "linear",
                      position: "bottom"
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero:false
                        }
                    }]
                }
            }
        });
      });
    }

    for(var i = 0; i < data.length; i++) {
      addOption(data[i].source_id, data[i].source_name);
    }
  });

}

function addOption(id, name) {
  var newOption = document.createElement("option");
  newOption.innerHTML = name + " (id=" + id + ")";
  newOption.onclick = function() {
    xData = [];
    xSource = id;
    getDataBySource(id, function(data) {
      for(let i = 0; i < data.results.length; i++) {
        xData.push(data.results[i].value);
      }
      updateChart();
    });
  }
  $("#dataSource").append(newOption);
}

function updateChart() {
  var mergedData = [];
  for(let i = 0; i < xData.length; i++) {
    mergedData.push({"x": xData[i], "y": yData[i]});
  }

  mergedData.sort(function(a,b) {
    return a.x - b.x;
  })

  myChart.data.datasets[0].data = mergedData;
  myChart.update(0);
}
