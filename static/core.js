/**
 * Created by jejemoreau on 07/01/2017.
 */

var app = angular.module('tickRecorder', []).controller('indexController',function ($scope,$http) {
    $scope.thread = {'status':false};
    $scope.keys = {'account_id':'', 'token':''};

    var threadStatus = function () {
        $http.get('http://localhost:80/is_alive').then(function (response) {
            console.log(response)
            if (response.data == true) {
                $scope.thread.status = true;
            }
        },function (reason) {
            console.warn(reason)
        })
    }

    $scope.setKeys = function(){
        console.log('changing keys')
        $http({
            url:'http://localhost:80/setkeys',
            method:'POST',
            data: $scope.keys
        })
    };

    var getKeys = function () {
        $http.get('http://localhost:80/getkeys').then(function (response) {
            console.log(response)
            $scope.keys.account_id = response.data.account_id;
            $scope.keys.token = response.data.token;
        },function (reason) {
            console.warn(reason)
        })
    }

    threadStatus();
    getKeys();
});