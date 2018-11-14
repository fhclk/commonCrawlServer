app.controller('dashboard', function($rootScope, $scope, $timeout, $location, $http) {

    $scope.userId = $rootScope.variable.userId;

    $scope.allTasks = [];
    $scope.waitingTasks = [];
    $scope.runningTasks = [];
    $scope.finishedTasks = [];
    $scope.jobLogLines = [];

    $scope.showCommonModal = { title: '', content: '' };
    $scope.runTaskForm = {};

    $scope.runTaskMessage = '';
    $scope.runTaskResult = false;
    // $scope.stopTaskMessage = '';
    $scope.stopTaskResult = false;


    var loadAllTasks = function() {
        $http.post("/crawlSetting/dashboard/loadAllTasks", { 'userId': $scope.userId })
            .success(function(response) {
                if (response.result) {
                    $scope.allTasks = response.data;
                }
            });
    }

    var loadWaitingTasks = function() {
        $http.post("/crawlSetting/dashboard/loadWaitingTasks", { 'userId': $scope.userId })
            .success(function(response) {
                if (response.result) {
                    $scope.waitingTasks = response.data;
                }
            });
    }

    var loadRunningTasks = function() {
        $http.post("/crawlSetting/dashboard/loadRunningTasks", { 'userId': $scope.userId })
            .success(function(response) {
                if (response.result) {
                    $scope.runningTasks = response.data;
                }
            });
    }

    var loadFinishedTasks = function() {
        $http.post("/crawlSetting/dashboard/loadFinishedTasks", { 'userId': $scope.userId })
            .success(function(response) {
                if (response.result) {
                    $scope.finishedTasks = response.data;
                }
            });
    }

    var loadData = function() {
        loadAllTasks();
        loadWaitingTasks();
        loadRunningTasks();
        loadFinishedTasks();
    }

    loadData();


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
    }

    $scope.runTask = function(task) {
        $scope.runTaskMessage = '';
        $scope.runTaskResult = false;
        $scope.runTaskForm = {};
        $scope.runTaskForm['crawl_no'] = (new XDate()).toString("yyyyMMddHHmmssfff");
        $scope.runTaskForm['task_no'] = task['task_no'];
        $scope.runTaskForm['task_type'] = task['task_type'];
        $scope.runTaskForm['priority'] = "0";
        $scope.runTaskForm['spider_type_value'] = "0";
        $('#job-run-modal').modal('show');
    };

    $scope.realRunTask = function() {
        var spiderTypeDict = {
            "0":"常规",
            "1":"模拟登录",
            "2":"模拟浏览器",
            "3":"代理"
        };
        var priorityDict = {
            "-1":"低",
            "0":"正常",
            "1":"高",
            "2":"较高"
        };
        var param = { 
            'userId': $scope.userId, 
            'taskNo': $scope.runTaskForm.task_no,
            'crawlNo' : $scope.runTaskForm.crawl_no,
            'taskType' : $scope.runTaskForm.task_type,
            'spiderType' : spiderTypeDict[$scope.runTaskForm.spider_type_value],
            'priority' : $scope.runTaskForm.priority
            // 'priority' : priorityDict[$scope.runTaskForm.priority]
        };
        if ($scope.runTaskForm.download_delay && $scope.runTaskForm.download_delay > 0) {
            param['downloadDelay'] = $scope.runTaskForm.download_delay;
        }
        $http.post("/crawlSetting/dashboard/runTask", param)
            .success(function(response) {
                $scope.runTaskMessage = response.message;
                $scope.runTaskResult = response.result;
                if (response.result) {
                    $timeout(function() {
                        $('#job-run-modal').modal('hide');
                    }, 1000);
                }
            });
    };

    $scope.cancelRunTask = function(job) {
        $('.message-alert').css('display','block');
        $http.post("/crawlSetting/dashboard/stopTask", {'userId': $scope.userId, "jobId":job.crawl_no, "scrapyJobId":job.scrapy_job_id})
            .success(function(response) {
                $scope.stopTaskMessage = response.message;
                $scope.stopTaskResult = response.result;
                if (response.result) {
                    $timeout(function() {
                        $('#message-alert-top').alert('close');
                    }, 1000);
                }
            });
    };

    $scope.showJobLog = function(job) {
        $http.post("/crawlSetting/dashboard/getJobLog", {'userId': $scope.userId, "spiderName":job.spider_name, "scrapyJobId":job.scrapy_job_id})
            .success(function(response) {
                if (response.result) {
                    $scope.logJob = job;
                    $scope.jobLogLines = response.data;
                    // $scope.jobLogLines = ['a', 'b', 'c'];
                    $('#show-job-log-modal').modal('show');
                }
            });
    };

    $scope.showJobResult = function(job) {
        $http.post("/crawlSetting/dashboard/getJobResult", {'userId': $scope.userId, "taskNo":job.task_no, "jobId":job.crawl_no})
            .success(function(response) {
                if (response.result) {
                    $scope.resultJob = job;
                    $scope.jobResultLines = response.data;
                    $scope.jobResultLinesJson = "<pre><code>" + JSON.stringify($scope.jobResultLines, null, '    ') + "</code></pre>";
                    $scope.jobResultType = response["task_type"];
                    console.dir(response);
                    // $scope.jobLogLines = ['a', 'b', 'c'];
                    $('#show-job-result-modal').modal('show');
                }
            });
    };

});