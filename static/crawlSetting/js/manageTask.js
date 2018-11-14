/**
 * Created by fhclk on 2018/2/23.
 */


app.controller('manageTask', function($rootScope, $scope, $timeout, $location, $http) {

    $scope.userId = $rootScope.variable.userId;
    $scope.allTasks = [];

    $scope.showCommonModal = { title: '', content: '' };

    var loadAllTasks = function() {
        $http.post("/crawlSetting/dashboard/loadAllTasks", { 'userId': $scope.userId })
            .success(function(response) {
                if (response.result) {
                    $scope.allTasks = response.data;
                }
            });
    };

    loadAllTasks();

    $scope.showTaskConfig = function(taskNo) {
        $scope.showCommonModal = {};
        $http.post("/crawlSetting/dashboard/getTaskConfig", { 'userId': $scope.userId, 'taskNo': taskNo })
            .success(function(response) {
                if (response.result) {

                    $scope.showCommonModal.title = "任务 " + taskNo + "的配置";
                    $scope.showCommonModal.content = "<pre><code>" + JSON.stringify(response.data, null, '    ') + "</code></pre>";
                    $('#showCommonModal').modal('show');
                }
            });
    };

    $scope.deleteTask = function (taskNo, index) {
        $('.message-alert').css('display','block');
        $http.post("/crawlSetting/manageTask/deleteTask", { 'userId': $scope.userId, 'taskNo': taskNo })
            .success(function(response) {
                if (response.result) {
                    $scope.allTasks.splict(index,1);
                }
                $scope.messageResult = response.result;
                $scope.messageContent = response.message;
            });
    }

    $scope.resetTask = function (task) {
        $http.post("/crawlSetting/dashboard/getTaskConfig", { 'userId': $scope.userId, 'taskNo': task.task_no })
            .success(function(response) {
                if (response.result) {
                    $scope.needResetTaskConfig = JSON.stringify(response.data, null, '    ');
                    $('#resetTaskConfig').modal('show');
                }
            });
    };

    $scope.saveResetTaskConfig = function() {
        $('.message-alert').css('display','block');
        var newConfig = {};
        try{
            newConfig = JSON.parse($scope.needResetTaskConfig);
        }catch(error){
            alert('修改后的JSON错误，请您检查');
            console.log("json错误" + str(error));
            return;
        }
        if (newConfig) {
            $http.post("/crawlSetting/manageTask/resetTask", { 'userId': $scope.userId, "taskConfig": JSON.stringify(newConfig)  })
            .success(function(response) {
                if (response.result) {
                    $scope.messageResult = true;
                    $scope.messageContent = response.message;
                }
                else {
                    $scope.messageResult = false;
                    $scope.messageContent = response.message;
                }
            });
        }
    }
});

