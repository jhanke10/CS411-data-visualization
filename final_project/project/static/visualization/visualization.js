xSource1 = null;
xData1 = [];
yData1 = [];

xSource2 = null;
xData2 = [];
yData2 = [];

myChart = null;

window.onload = function(e) {

  setInterval(function() {
    getDataBySource(xSource1, function(dat) {
      xData1 = [];
      yData1 = [];
      for(let i = 0; i < dat.results.length; i++) {
        xData1.push(dat.results[i].create_time);
        yData1.push(dat.results[i].value);
      }

      updateChart();
    });

    getDataBySource(xSource2, function(dat) {
      xData2 = [];
      yData2 = [];
      for(let i = 0; i < dat.results.length; i++) {
        xData2.push(dat.results[i].create_time);
        yData2.push(dat.results[i].value);
      }

      updateChart();
    });
  }, 200);

  getAllSources(function(data) {
    //console.log(JSON.stringify(data));

    if(data.length > 0) {
      xSource1 = data[0].source_id;
      xSource2 = null;
      getDataBySource(xSource1, function(dat) {
        for(let i = 0; i < dat.results.length; i++) {
          xData1.push(dat.results[i].create_time);
          yData1.push(dat.results[i].value);
        }

        var mergedData = [];
        for(let i = 0; i < xData1.length; i++) {
          mergedData.push({"x": xData1[i], "y": yData1[i]});
        }

        myChart = new Chart($("#dataVisChart"), {
            type: 'line',
            data: {
                label: "WIP",
                datasets: [
                  {
                    label: 'Source 1',
                    data: mergedData
                  },
                  {
                    label: 'Source 2'
                  },
                  {}
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
    xData1 = [];
    xSource1 = id;
    getDataBySource(id, function(data) {
      for(let i = 0; i < data.results.length; i++) {
        xData1.push(data.results[i].value);
      }
      updateChart();
    });
  }

  var newOption2 = document.createElement("option");
  newOption2.innerHTML = name + " (id=" + id + ")";
  newOption2.onclick = function() {
    xData2 = [];
    xSource2 = id;
    getDataBySource(id, function(data) {
      for(let i = 0; i < data.results.length; i++) {
        xData2.push(data.results[i].value);
      }
      updateChart();
    });
  }
  $("#dataSource").append(newOption);
  $("#dataSource2").append(newOption2);
}

function updateChart() {
  var mergedData = [];
  for(let i = 0; i < xData1.length; i++) {
    mergedData.push({"x": xData1[i], "y": yData1[i]});
  }

  mergedData.sort(function(a,b) {
    return a.x - b.x;
  })

  var mergedData2 = [];
  for(let i = 0; i < xData2.length; i++) {
    mergedData2.push({"x": xData2[i], "y": yData2[i]});
  }

  mergedData2.sort(function(a,b) {
    return a.x - b.x;
  })

  myChart.data.datasets[0].data = mergedData;
  myChart.data.datasets[1].data = mergedData2;
  myChart.update(0);
}

function runCompare() {
  postCompare(xSource1, xSource2, function(dat) {
    var data = dat.data;
    console.log(JSON.stringify(data));
    var mergedData = [];
    for(let i = 0; i < data.length; i++) {
      mergedData.push({"x": data[i].create_time, "y": data[i].difference});
    }
    console.log(mergedData);
    mergedData.sort(function(a,b) {
      return a.x - b.x;
    })
    console.log(mergedData);

    myChart.data.datasets[2] = ({
      type: "line",
      fill: false,
      label: "Absolute difference",
      data: mergedData,
      borderColor: "#0000FF",
      pointBorderColor: "#FF0000"
    });
    myChart.update(0);
  })
}
