angular.module('tasksApp', [])
    .controller('TasksController', function($scope) {
        $scope.tasks = [
            {assignee: 'Adi Levin', description:'Prepare presentation', done:false},
            {assignee: 'Adi Levin', description:'Write code', done:false},
            {assignee: 'Adi Levin', description:'Eat lunch', done:false}];
        $scope.getTasks = function() {
            return this.tasks;
        };
        $scope.refreshFromServer = function() {
            alert('Refreshing from server');
        };
        $scope.doneClicked = function() {
            alert('Done clicked');
        }
        $scope.new_task_description='';
        $scope.addTask = function() {
            $scope.tasks.push(
                {assignee:$scope.assignee,description:$scope.new_task_description,done:false}
            )
            $scope.new_task_description='';
        }
        $scope.assignee = 'Adi Levin';
        $scope.new_assignee = $scope.assignee;
        $scope.setNewAssignee = function() {
            $scope.assignee = $scope.new_assignee;
        }
    });