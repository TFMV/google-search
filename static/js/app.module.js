(function() {
  angular
    .module('App', ['angularjs-dropdown-multiselect', 'ngAnimate', 'ui.bootstrap'])
    .config(function($interpolateProvider) {
      $interpolateProvider.startSymbol('[[');
      $interpolateProvider.endSymbol(']]');
    })
    .controller('AppController', AppController);

    AppController.$inject = ['$scope', '$http'];
    function AppController($scope, $http) {
      //control data
      $scope.dataIsLoading = false;
      $scope.error = false;

      //user data
      $scope.recievedData = null;
      $scope.selectedTerm = null;
      $scope.tableData = null;

      $scope.sendTerm = sendTerm;
      $scope.send =  send;
      $scope.changeCounters = changeCounters;
      $scope.limit = parseInt(document.getElementById('remainig').innerHTML) == 0;

      function changeCounters() {
        var today = document.getElementById('today');
        var remaining = document.getElementById('remainig');
        today.innerHTML = parseInt(today.innerHTML) + 1;
        remaining.innerHTML = parseInt(remaining.innerHTML) - 1;
      }
      //cload

      function sendTerm() {
        var el = document.getElementById("terms");
        if (el.selectedIndex == -1)
          console.log('NULL');

        $scope.selectedTerm = el.options[el.selectedIndex].text;
        console.log('RUN');

        $scope.send();
      }

      function send() {
        $http.post('/api/v1/search/', { terms: [$scope.selectedTerm] })
              .then(function(res) {
                console.log('HERE');
                $scope.tableData = res.data.data.result[0].urls;
                $scope.changeCounters();
              })
              .catch(function() {
                console.log('Error!');
              });
      }
    }
})();
