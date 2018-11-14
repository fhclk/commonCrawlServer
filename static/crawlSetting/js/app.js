var app = angular.module('crawlSetting', []);
app.config(function($httpProvider) {

    $httpProvider.defaults.transformRequest = function(obj) {
        var str = [];
        for (var p in obj) {
            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        }
        return str.join("&");
    }

    $httpProvider.defaults.headers.post = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

});

app.run(function ($rootScope) {
        $rootScope.variable = {
            userId : 'abcdefghijk0004'
        };
    });


app.filter('trustHtml', function($sce) {
    return function(input) {
        return $sce.trustAsHtml(input);
    }
});