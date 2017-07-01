'use strict';

var app = angular.module('sampleapp', ['ngRoute', 'ngCookies']);
app.config(function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'static/views/chat_view.html',
            controller: 'ChatCtrl'
        })
        .otherwise({
            redirectTo: '/'
        });
});
