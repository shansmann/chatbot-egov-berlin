'use strict';

var app = angular.module('sampleapp', ['ngRoute', 'ngCookies'])
    .directive('onFinishRender', function($timeout) {
        return {
            restrict: 'A',
            link: function(scope, element, attr) {
                if (scope.$last === true) {
                    $timeout(function() {
                        scope.$emit(attr.onFinishRender);
                    });
                }
            }
        }
    });

app.service('Auth', function() {

    this.loggedIn = false

    this.login = function (user, pw) {
        if (user == 'admin' && pw == 'berlina') {
          this.loggedIn = true
        }
        return this.loggedIn;
    }

    this.status = function(){
      return this.loggedIn;
    }

});

var onlyLoggedIn = function($location, $q, Auth) {
    var deferred = $q.defer();

    if (Auth.loggedIn) {
        deferred.resolve();
    } else {
        deferred.reject();
        $location.url('/');
    }
    return deferred.promise;
    //return true;
};

app.config(function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'static/views/login.html',
            controller: 'LoginCtrl',
        })
        .when('/dashboard', {
            templateUrl: 'static/views/dashboard.html',
            controller: 'DashboardCtrl',
            resolve: {
              loggedIn:onlyLoggedIn
            }
        })
        .otherwise({
            redirectTo: '/'
        });
});
