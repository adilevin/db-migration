function generate_new_task_description() {
    return 'A random task';
}

function User(name) {
    this.name = name;
    this.num_of_uncompleted_tasks = 0;
    this.healthy_task_post = true;
    this.healthy_task_get = true;
    this.healthy_task_put = true;
}

var http_timeout_milliseconds = 1000;
var interval_for_marking_tasks_as_done_milliseconds = 6000;
var interval_for_creating_new_task_milliseconds = 500;

User.prototype.is_healthy = function() {
    return (this.healthy_task_post && this.healthy_task_get && this.healthy_task_put);
};

angular.module('tasksApp', [])
    .controller('TasksController', function($scope,$http,$httpParamSerializerJQLike,$interval,$timeout) {
        $scope.is_active = false;
        $scope.max_num_of_tasks_to_display = 20;
        $scope.assignees = [new User('Bill'), new User('Ronald')];
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
                timeout: http_timeout_milliseconds,
                data: $httpParamSerializerJQLike({
                    assignee: assignee.name,
                    description: generate_new_task_description()
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(
                function onSuccess(result) { assignee.healthy_task_post = true; },
                function onError(result) { assignee.healthy_task_post = false; }
            ).finally(
                function() { $timeout(function(){$scope.create_new_task_for(assignee)},interval_for_creating_new_task_milliseconds); }
            );
        };
        $scope.refresh_task_count_for = function(assignee) {
            if (!$scope.is_active)
                return;
            $http.get('http://localhost:5000/tasks?done=False&assignee=' + encodeURI(assignee.name),{timeout:http_timeout_milliseconds}).then(
                function onSuccess(result){
                    assignee.healthy_task_get = true;
                    assignee.num_of_uncompleted_tasks = result.data.length;
                },
                function onError(result) { assignee.healthy_task_get = false; }
            ).finally(
                function() { $timeout(function(){$scope.refresh_task_count_for(assignee)},500);}
            );
        };
        $scope.mark_tasks_done_for = function(assignee) {
            if (!$scope.is_active)
                return;
            $http.get('http://localhost:5000/tasks?done=False&assignee=' + encodeURI(assignee.name),{timeout:http_timeout_milliseconds}).then(
                function onSuccess(result) {
                    assignee.healthy_task_put = true;
                    result.data.forEach(function (task) {
                        $http.put('http://localhost:5000/tasks/' + task.id).catch(function() {
                            assignee.healthy_task_put = false;
                        });
                    });
                },
                function onError(result) { assignee.healthy_task_get = false; }
            ).finally(
                function () {
                    $timeout(function () {
                        $scope.mark_tasks_done_for(assignee);
                    }, interval_for_marking_tasks_as_done_milliseconds);
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
