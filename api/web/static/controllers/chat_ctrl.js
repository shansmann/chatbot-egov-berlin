'use strict';

app.controller('ChatCtrl', function ($rootScope, $scope, $route, $http, $cookies) {
    $rootScope.conversation = [];
    $scope.newPostBot = {};
    $scope.user_name = 'User';
    $scope.user_id = $cookies.get('user_id');
    if (!$scope.user_id) {
        $scope.user_id = 1;
    }

    $scope.postNew = function(){
        if($scope.newPost){
            $scope.newPost.sender = {"id": $scope.user_id, "name": $scope.user_name};
            $scope.newPost.date = Date();
            $rootScope.conversation.push($scope.newPost);
            $http.post('/webhook', $scope.newPost).then(function(response){
                $scope.newPostBot = {};
                $scope.newPost = {};
                if (!response.data.message.text) return;
                $scope.newPostBot.sender = {"id": "bot", "name": "Bot"};
                $scope.newPostBot.date = response.data.ts;
                $scope.newPostBot.message = response.data.message;
                $rootScope.conversation.push($scope.newPostBot);
                $scope.newPostBot = {};
            }).catch(function(error){
                console.log(error);
            });
        }
    };
});
