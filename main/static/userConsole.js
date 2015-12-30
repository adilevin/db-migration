var http_timeout_milliseconds = 1000;

angular.module('tasksApp')
    .controller('TasksController', function($scope,$http,$httpParamSerializerJQLike,$timeout) {
        $scope.tasks = [];
        $scope.reloadTaskListFromServer = function() {
            if ($scope.assignee=='') {
                $scope.tasks = {}
                $timeout(function () {
                    $scope.reloadTaskListFromServer();
                }, 1000);
            } else {
                $http.get('/tasks?done=False&assignee=' + encodeURI($scope.assignee),{timeout:http_timeout_milliseconds}).then(
                    function onSuccess(result) {
                        $scope.tasks = result.data;
                    },
                    function onError(result) {});
            }
        };
        $scope.markTaskAsDone = function(task_id) {
            $http.put('/tasks/' + task_id,{timeout:http_timeout_milliseconds}).then(
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
                    timeout:http_timeout_milliseconds,
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
    });