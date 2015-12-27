function generate_new_task_description()
{
    return 'A random task';
}

angular.module('tasksApp', [])
    .controller('TasksController', function($scope,$http,$httpParamSerializerJQLike,$interval) {
        $scope.max_num_of_tasks_to_display = 20;
        $scope.assignees = [
            {name:'John',num_of_uncompleted_tasks:0},
            {name:'James',num_of_uncompleted_tasks:0}
        ];
        $scope.num_http_failures = 0;
        $scope.max_num_http_failures_to_display = 20;
        $scope.percentage_of_http_failures = function() {
            var p = $scope.num_http_failures*100/$scope.max_num_http_failures_to_display;
            return Math.min(p,100)
        };
        $scope.percentage_of_uncompleted_tasks = function(assignee) {
            var p = assignee.num_of_uncompleted_tasks*100/$scope.max_num_of_tasks_to_display;
            return Math.min(p,100)
        };
        $scope.create_new_task_for = function(assignee_name) {
            $http({
                method: 'POST',
                url: 'http://localhost:5000/tasks',
                data: $httpParamSerializerJQLike({
                    assignee: assignee_name,
                    description: generate_new_task_description()
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(
                function onSuccess(result){ },
                function onError(result) { $scope.num_http_failures += 1;}
            );
        };
        $scope.refresh_task_count_for = function(assignee) {
          $http.get('http://localhost:5000/tasks?done=False&assignee=' + encodeURI(assignee.name)).then(
                function onSuccess(result){
                    assignee.num_of_uncompleted_tasks = result.data.length;
                },
                function onError(result) {
                    $scope.num_http_failures += 1;
                });
        };
        $scope.mark_tasks_done_for = function(assignee) {
          $http.get('http://localhost:5000/tasks?done=False&assignee=' + encodeURI(assignee.name)).then(
                function onSuccess(result){
                    result.data.forEach(function(task) {
                        $http.put('http://localhost:5000/tasks/' + task.id).then(
                            function onSuccess(result){ },
                            function onError(result) { $scope.num_http_failures += 1; });
                    });
                    $scope.num_http_failures = Math.floor($scope.num_http_failures/2);
                },
                function onError(result) {
                    $scope.num_http_failures += 1;
                });
        };
        $scope.produce_tasks = function() {
            $scope.assignees.forEach(function(assignee) {
                $scope.create_new_task_for(assignee.name);
            })
        };
        $scope.mark_tasks_as_done = function() {
            $scope.assignees.forEach(function(assignee) {
                $scope.mark_tasks_done_for(assignee);
            })
        };
        $scope.refresh_task_count = function() {
            $scope.assignees.forEach(function(assignee) {
                $scope.refresh_task_count_for(assignee);
            })
        };
        $interval(function(){$scope.refresh_task_count()},1000);
        $interval(function(){$scope.produce_tasks()},1000);
        $interval(function(){$scope.mark_tasks_as_done()},5000);
    });
