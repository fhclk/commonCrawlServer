app.controller('createTask', function($rootScope, $scope, $timeout, $location, $http) {


    $scope.userId = $rootScope.variable.userId;

    $scope.is_upload_image = false;
    $scope.is_replace_img_src = false;


    var followCount = 0;
    var ruleCount = 0;

    function initData() {
        $scope.taskConfig = {};
        $scope.taskConfig.task_no = (new XDate()).toString("yyyyMMddHHmmss");
        $scope.taskConfig.upload_image = {};
        $scope.taskConfig.replace_img_src = {};
        $scope.taskConfig.follows = [];
        $scope.taskConfig.url_rules = [];
        followCount = 0;
        ruleCount = 0;
    }

    initData();


    $scope.$watch('$viewContentLoaded', function() {
        if (sessionStorage.createdTaskConfig) {
            taskConfig = JSON.parse(sessionStorage.createdTaskConfig);
            if (taskConfig.start_url || taskConfig.follows.length > 0) {
                $scope.taskConfig = taskConfig;
            }
        }
    });


    $scope.addOrderlyListFollow = function() {
        var orderlyListFollow = {
            ord: followCount,
            type: "orderly_list",
            has_next_page: false,
            next_page_ord: 0,
            selector1: "",
            selector2: "",
            link_selector: "",
            next_follow_ord: 2.0,
            columns: []
        };
        $scope.taskConfig.follows.push(orderlyListFollow);
        followCount++;
    };

    $scope.addDisorderedListFollow = function() {
        var disorderedListFollow = {
            ord: followCount,
            type: "disordered_list",
            list: [
                // {
                //  selector: "",
                //     next_follow_ord: 0,
                //     link_selector: "",
                //     columns : []
                // }
            ],
            has_next_page: false,
            next_page_ord: 0,
        };
        $scope.taskConfig.follows.push(disorderedListFollow);
        followCount++;
    };

    $scope.addNextPageFollow = function() {
        var nextPageFollow = {
            ord: followCount,
            type: "next_page",
            next_follow_ord: 0,
            link_selector: ""
        };
        $scope.taskConfig.follows.push(nextPageFollow);
        followCount++;
    };

    $scope.addSinglePageFollow = function() {
        var singlePageFollow = {
            ord: followCount,
            type: "single_page",
            has_next_page: false,
            next_page_ord: 0,
            columns: []
        };
        $scope.taskConfig.follows.push(singlePageFollow);
        followCount++;
    };

    $scope.addRules = function() {
        var rule = {
            ord: ruleCount,
            need_parse: false,
            columns: []
        };
        $scope.taskConfig.url_rules.push(rule);
        ruleCount++;
    };

    // $scope.addOrderlyListColumn = function(follow) {
    //     var column = {
    //         selector: "",
    //         name: "",
    //         disable: "",
    //         condition: {}
    //     };
    //     follow.columns.push(column);
    // };


    // $scope.addDisorderedListColum = function(item) {
    //     var column = {
    //         selector: "",
    //         name: "",
    //         disable: "",
    //         condition: {}
    //     };
    //     item.columns.push(column);
    // };

    $scope.addDisorderedListItem = function(follow) {
        var item = {
            selector: "",
            next_follow_ord: 0,
            link_selector: "",
            columns: []
        };
        follow.list.push(item);
    };

    $scope.showJson = function(data) {
        var newData = angular.copy(data);
        return JSON.stringify(newData, null, '    ');
    };

    $scope.saveTaskConfig = function() {
        console.log('saveTaskConfig');
        if ($scope.taskConfig.task_type == 'normal_spider') {
            delete $scope.taskConfig.url_rules;
        }
        if ($scope.taskConfig.task_type == 'rule_spider') {
            delete $scope.taskConfig.follows;
             angular.forEach($scope.taskConfig.url_rules, function(rule) {
                rule.allow = rule.allow.split(';\r\n');
                rule.deny = rule.deny.split(';\r\n');
             });
        }
        var newData = angular.copy($scope.taskConfig);
        // var xmlhttp;
        // if (window.XMLHttpRequest) {
        //     // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
        //     xmlhttp = new XMLHttpRequest();
        // } else {
        //     // IE6, IE5 浏览器执行代码
        //     xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        // }
        // xmlhttp.onreadystatechange = function() {
        //     if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        //         var response = JSON.parse(xmlhttp.responseText);
        //         $scope.toDoResult = response.result;
        //         $scope.toDoMessage = response.message;
        //         if (response.result) {
        //             $timeout(function() {
        //                 // initData();
        //                 // $scope.toDoMessage = '';
        //                 sessionStorage.createdTaskConfig = '';
        //                 window.navigate('/crawlSetting/dashboard.html');
        //             }, 2000);
        //         }
        //     }
        // }
        // xmlhttp.open("POST", "/crawlSetting/saveTaskConfig", true);
        // xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        // xmlhttp.send("userId="+$scope.userId+"&taskConfig=" + JSON.stringify(newData));

        $http.post("/crawlSetting/saveTaskConfig", { 'userId': $scope.userId, "taskConfig": JSON.stringify(newData) })
            .success(function(response) {
                $scope.toDoResult = response.result;
                $scope.toDoMessage = response.message;
                if (response.result) {
                    $timeout(function() {
                        initData();
                        $scope.toDoMessage = '';
                        sessionStorage.createdTaskConfig = '';
                    }, 1400);
                }
            });
    }

    $scope.createTask = function() {
        var checkMsg = checkFilledData();
        if (checkMsg) {
            $scope.toDoResult = false;
            $scope.toDoMessage = checkMsg;
            return;
        }
        $http.post("/crawlSetting/createTaskConfig", { 'userId': $scope.userId, "taskConfig": JSON.stringify(newData) })
            .success(function(response) {
                $scope.toDoResult = response.result;
                $scope.toDoMessage = response.message;
                if (response.result) {
                    $timeout(function() {
                        initData();
                        $scope.toDoMessage = '';
                        sessionStorage.createdTaskConfig = '';
                    }, 1400);
                }
            });
    };

    $scope.cleanFillData = function() {
        initData();
        sessionStorage.createdTaskConfig = '';
    }


    var checkFilledData = function() {
        if (!$scope.taskConfig.start_url) {
            return '没有填写待爬取的网站的地址';
        }
        if ($scope.taskConfig.follows.length > 0) {
            angular.forEach($scope.taskConfig.follows, function(follow) {
                if (follow.type == 'orderly_list') {
                    if (!follow.selector1) {
                        return '没有填写列表item1的xpath';
                    }
                    if (!follow.selector1) {
                        return '没有填写列表item2的xpath';
                    }
                    if (!follow.link_selector) {
                        return '没有填写列表item1链接xpath';
                    }
                    if (follow.columns && follow.columns.length > 0) {
                        angular.forEach(follow.columns, function(column) {
                            if (!column.name) {
                                return '没有填写要爬取内容的字段的name';
                            }
                            if (!column.selector) {
                                return '没有填写要爬取内容的字段的xpath';
                            }
                        });
                    }
                }
                if (follow.type == 'disordered_list') {
                    if (follow.list && follow.list.length > 0) {
                        if (!follow.link_selector) {
                            return '没有填写列表item的链接xpath';
                        }
                        if (follow.columns && follow.columns.length > 0) {
                            angular.forEach(follow.columns, function(column) {
                                if (!column.name) {
                                    return '没有填写要爬取内容的字段的name';
                                }
                                if (!column.selector) {
                                    return '没有填写要爬取内容的字段的xpath';
                                }
                            });
                        }
                    }
                }
                if (follow.type == 'next_page') {
                    if (!follow.link_selector) {
                        return '没有填写下一页的链接的xpath';
                    }
                }
                if (follow.type == 'single_page') {
                    if (follow.columns && follow.columns.length > 0) {
                        angular.forEach(follow.columns, function(column) {
                            if (!column.name) {
                                return '没有填写要爬取内容的字段的name';
                            }
                            if (!column.selector) {
                                return '没有填写要爬取内容的字段的xpath';
                            }
                        });
                    }

                }
            });
        }
    }


    window.onbeforeunload = function(e) {
        if ($scope.taskConfig.start_url || $scope.taskConfig.follows.length > 0) {
            sessionStorage.createdTaskConfig = JSON.stringify($scope.taskConfig);
        }
    };

});