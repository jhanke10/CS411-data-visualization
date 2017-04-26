xData = [];
xSource = null;
yData = [];
ySource = null;

myChart = null;

window.onload = function(e) {

  getAllSources(function(data) {
    //console.log(JSON.stringify(data));

    if(data.length > 0) {
      xSource = data[0].source_id;
      ySource = data[0].source_id;
      getDataBySource(xSource, function(dat) {
        for(let i = 0; i < dat.results.length; i++) {
          xData.push(dat.results[i].value);
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
                  },
                  {
                    label: '',
                    data: []
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
                            beginAtZero:true
                        }
                    }]
                }
            }
        });
      });
    }

    for(var i = 0; i < data.length; i++) {
      addXOption(data[i].source_id, data[i].source_name);
      addYOption(data[i].source_id, data[i].source_name);
    }
  });

  function addData(time, value) {
    myChart.data.labels.push(time);
    myChart.data.datasets[0].data.push(value);
    myChart.update(100);
  }

}

function addXOption(id, name) {
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
  $("#xAxis").append(newOption);
}

function addYOption(id, name) {
  var newOption = document.createElement("option");
  newOption.innerHTML = name + " (id=" + id + ")";
  newOption.onclick = function() {
    yData = [];
    ySource = id;
    getDataBySource(id, function(data) {
      for(let i = 0; i < data.results.length; i++) {
        yData.push(data.results[i].value);
      }
      updateChart();
    });
  }
  $("#yAxis").append(newOption);
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
  myChart.data.datasets[1] = {};
  myChart.update(0);
}

function runLinearRegression() {
  var count = parseInt($("#count").val());
  postLinearData(xData, yData, count, function(data) {
    regressYData = [];
    var p = data.coefficients;
    for(let i = 0; i < xData.length; i++) {
      y = 0;
      for(let j = 0; j < count + 1; j++) {
        y += p[j] * (Math.pow(xData[i], count - j));
      }
      regressYData.push(y);
    }
    var mergedData = [];
    for(let i = 0; i < xData.length; i++) {
      mergedData.push({"x": xData[i], "y": regressYData[i]});
    }
    mergedData.sort(function(a,b) {
      return a.x - b.x;
    })

    myChart.data.datasets[1] = ({
      type: "line",
      fill: false,
      label: "Regression (k=" + count + ")",
      data: mergedData,
      borderColor: "#FF0000",
      pointBorderColor: "#FF0000"
    });
    myChart.update(0);
  });
}



function runCompare() {
  postCompare(xSource, ySource, function(data) {
    console.log(JSON.stringify(data));
  })
}
