'use strict';

app.controller('DashboardCtrl', function($rootScope, $scope, $route, $http, $cookies) {

    $scope.messages = []

    // retrieve data from database and prepare plot
    $scope.getData = function() {

        $http.get('/topic').then(function(response) {

            //console.log(response.data)
            var parsed_data = $scope.parseData(response.data)

            console.log('topic data: ' + parsed_data)

            $scope.renderChart("topicChart", parsed_data[0], parsed_data[1])

        })

        $http.get('/detail').then(function(response) {

            //console.log(response.data)
            var parsed_data = $scope.parseData(response.data)

            console.log('detail data: ' + parsed_data)

            $scope.renderChart("detailChart", parsed_data[0], parsed_data[1])

        })
    }

    // parse data
    $scope.parseData = function(data) {
      var labels = []
      var counts = []
      for (var key in data) {
        labels.push(key)
        counts.push(data[key])
      }
        return [labels, counts]
    }

    // create random color
    function getRandomColor() {
      var letters = '0123456789ABCDEF'.split('');
      var color = '#';
      for (var i = 0; i < 6; i++ ) {
          color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }

    // render chart
    $scope.renderChart = function(id, labels, counts) {
      var ctx = document.getElementById(id);
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                borderColor : "white",
                backgroundColor: ["#c7d9ff", "#253276", "#b5050e", "grey"],
            }]
        },
        options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]
          },
          legend: {
            display: false
         },
        }
      });
    }

    // main

    $scope.getData()

});
