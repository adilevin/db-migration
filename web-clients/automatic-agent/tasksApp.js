function generate_new_task_description() {
    return 'A random task';
}

angular.module('tasksApp', [])
    .controller('TasksController', function($scope,$http,$httpParamSerializerJQLike,$interval,$timeout) {
        $scope.is_active = false;
        $scope.max_num_of_tasks_to_display = 20;
        $scope.assignees = [
            {name:'John',num_of_uncompleted_tasks:0,is_healthy:true},
            {name:'James',num_of_uncompleted_tasks:0,is_healthy:true}
        ];
        $scope.percentage_of_uncompleted_tasks = function(assignee) {
            var p = assignee.num_of_uncompleted_tasks*100/$scope.max_num_of_tasks_to_display;
            return Math.min(p,100)
        };
        $scope.create_new_task_for = function(assignee) {
            if (!$scope.is_active)
                return;
            $http({
                method: 'POST',
                url: 'http://localhost:5000/tasks',
                data: $httpParamSerializerJQLike({
                    assignee: assignee.name,
                    description: generate_new_task_description()
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(
                function onSuccess(result) { assignee.is_healthy = true; },
                function onError(result) { assignee.is_healthy = false; }
            ).finally(
                function() { $timeout(function(){$scope.create_new_task_for(assignee)},100); }
            );
        };
        $scope.refresh_task_count_for = function(assignee) {
            if (!$scope.is_active)
                return;
            $http.get('http://localhost:5000/tasks?done=False&assignee=' + encodeURI(assignee.name)).then(
                function onSuccess(result){
                    assignee.is_healthy = true;
                    assignee.num_of_uncompleted_tasks = result.data.length;
                },
                function onError(result) { assignee.is_healthy = false; }
            ).finally(
                function() { $timeout(function(){$scope.refresh_task_count_for(assignee)},0);}
            );
        };
        $scope.mark_tasks_done_for = function(assignee) {
            if (!$scope.is_active)
                return;
            $http.get('http://localhost:5000/tasks?done=False&assignee=' + encodeURI(assignee.name)).then(
                function onSuccess(result) {
                    assignee.is_healthy = true;
                    result.data.forEach(function (task) {
                        $http.put('http://localhost:5000/tasks/' + task.id);
                    });
                },
                function onError(result) { assignee.is_healthy = false; }
            ).finally(
                function () {
                    $timeout(function () {
                        $scope.mark_tasks_done_for(assignee);
                    }, 2000);
                }
            );
        };
        $scope.activate = function() {
            $scope.is_active = true;
            $scope.assignees.forEach(function(assignee) {
                $scope.create_new_task_for(assignee);
                $scope.mark_tasks_done_for(assignee);
                $scope.refresh_task_count_for(assignee);
            });
        };

        $scope.deactivate = function() {
            $scope.is_active = false;
        }
    });
