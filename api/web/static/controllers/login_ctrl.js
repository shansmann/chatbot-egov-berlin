'use strict';

app.controller('LoginCtrl', function($rootScope, $scope, $route, $http, $location, Auth) {

  $scope.login = function() {
    Auth.login($scope.user, $scope.pw)
    $location.url('/dashboard')
  }
});
