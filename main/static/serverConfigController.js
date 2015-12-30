
angular.module('tasksApp')
    .controller('serverConfigController', function($scope,$http,$timeout) {
        var http_timeout_milliseconds = 1000;
        $scope.server_config = {};
        $scope.config_has_changed = false
        $scope.server_config_state = function() {
            if ($scope.config_has_changed)
                return 'config_has_changed';
            else
                return '';
        };
        $scope.readServerConfig = function() {
            $http.get('/config',{timeout:http_timeout_milliseconds}).then(
                function onSuccess(result) {
                    new_server_config = JSON.stringify(result.data, undefined, 2);
                    $scope.config_has_changed = (new_server_config != $scope.server_config);
                    if ($scope.config_has_changed)
                        $scope.server_config = new_server_config;
                }
            ).finally(function(){
                    $timeout(function() {$scope.readServerConfig();},3000);}
            );
        };
        $scope.readServerConfig();
    });