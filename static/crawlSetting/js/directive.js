app.directive("columnsDirective", function() {
    return {
        restrict: "EA",
        scope: {
            columns: '=columns'
        },
        templateUrl: "columnsDirective.html",
        replace: true, // 使用模板替换原始标记 
        // transclude: false, // 不复制原始HTML内容 
        controller: ["$scope", function($scope) {
            $scope.addColumn = function(columns) {
                var column = {
                    selector: "",
                    name: "",
                    disable: "",
                    condition: {}
                };
                columns.push(column);
            }
        }],
        link: function(scope, element, attrs, controller) {

        }
    }
});

app.directive("panelToolsDirective", function() {
    return {
        restrict: "EA",
        scope: {
            follow: '=follow',
            follows: '='
        },
        template: "<div class='panel-tools'>" +
            "<img src='../static/image/hiddenItem.png' ng-click='hiddenPanelBody($event)'>" +
            "<img src='../static/image/deleteItem.png' ng-click='deleteFollow(follow)'></div>",
        replace: true, // 使用模板替换原始标记 
        // transclude: false, // 不复制原始HTML内容 
        controller: ["$scope", function($scope) {
            $scope.hiddenPanelBody = function($event) {
                var parentEl = event.target.parentElement;
                while (parentEl.className != "panel-heading") {
                    parentEl = parentEl.parentElement;
                }
                var panelBodyEl = parentEl.nextElementSibling;
                if (panelBodyEl) {
                    if (panelBodyEl.style.display == 'none') {
                        panelBodyEl.style.display = 'block'
                    } else {
                        panelBodyEl.style.display = 'none'
                    }
                }
            };
            $scope.deleteFollow = function(follow) {
                angular.forEach($scope.follows, function(value, index) {
                    if (follow.$$hashKey == value.$$hashKey) {
                        $scope.follows.splice(index, 1);
                    }
                })
            };
        }],
        link: function(scope, element, attrs, controller) {

        }
    }
});


app.directive("itemDeleteTool", function() {
    return {
        restrict: "EA",
        scope: {
            item: '=',
            items: '='
        },
        template: "<img class='item-delete-tool' src='../static/image/deleteItem1.png' ng-click='deleteItem(item)'>",
        replace: true,
        controller: ["$scope", function($scope) {
            $scope.deleteItem = function(follow) {
                angular.forEach($scope.items, function(value, index) {
                    if (follow.$$hashKey == value.$$hashKey) {
                        $scope.items.splice(index, 1);
                    }
                })
            };
        }]
    }
});

