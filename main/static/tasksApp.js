angular.module('tasksApp', [])
    .controller('TasksController', function($scope,$http,$httpParamSerializerJQLike) {
        $scope.tasks = [];
        $scope.server_config = {};
        $scope.readServerConfig = function() {
            $http.get('/config').then(
                function onSuccess(result){
                    $scope.server_config = JSON.stringify(result.data,undefined,2);
                }
            );
        };
        $scope.reloadTaskListFromServer = function() {
            $http.get('/tasks?done=False&assignee=' + encodeURI($scope.assignee)).then(
                function onSuccess(result){
                    $scope.tasks = result.data;
                },
                function onError(result) {
                    alert('http returned error');
                });
        };
        $scope.markTaskAsDone = function(task_id) {
            $http.put('/tasks/' + task_id).then(
                function onSuccess(result){
                    $scope.reloadTaskListFromServer();
                },
                function onError(result) {
                    alert('Http failed');
                });
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
                    function onError(result) {
                        alert('Http failed');
                    });
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