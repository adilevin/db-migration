angular.module('tasksApp', [])
    .controller('TasksController', function($scope,$http,$httpParamSerializerJQLike,$timeout) {
        $scope.tasks = [];
        $scope.server_config = {};
        $scope.config_has_changed = false
        $scope.server_config_state = function() {
            if ($scope.config_has_changed)
                return 'config_has_changed';
            else
                return '';
        };
        $scope.readServerConfig = function() {
            $http.get('/config').then(
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
        $scope.reloadTaskListFromServer = function() {
            if ($scope.assignee=='') {
                $scope.tasks = {}
                $timeout(function () {
                    $scope.reloadTaskListFromServer();
                }, 1000);
            } else {
                $http.get('/tasks?done=False&assignee=' + encodeURI($scope.assignee)).then(
                    function onSuccess(result) {
                        $scope.tasks = result.data;
                    },
                    function onError(result) {}).finally(
                function () {
                    $timeout(function () {
                        $scope.reloadTaskListFromServer();
                    }, 1000);
                }
            );;
            }
        };
        $scope.markTaskAsDone = function(task_id) {
            $http.put('/tasks/' + task_id).then(
                function onSuccess(result){
                    $scope.reloadTaskListFromServer();
                },
                function onError(result) {});
        }
        $scope.new_task_description='';
        $scope.addTask = function() {
            if ($scope.new_task_description!='') {
                $http({
                    method: 'POST',
                    url: '/tasks',
                    data: $httpParamSerializerJQLike({
                        assignee: $scope.assignee,
                        description: $scope.new_task_description
                    }),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                }).then(
                    function onSuccess(result){
                        $scope.new_task_description = '';
                        $scope.reloadTaskListFromServer();
                    },
                    function onError(result) {});
            }
        }
        $scope.assignee = '';
        $scope.new_assignee = $scope.assignee;
        $scope.setNewAssignee = function() {
            $scope.tasks = []
            $scope.assignee = $scope.new_assignee;
            $scope.reloadTaskListFromServer();
        }
        $scope.readServerConfig();
    });