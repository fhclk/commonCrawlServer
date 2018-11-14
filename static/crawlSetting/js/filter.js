/**
 * Created by fhclk on 2018/2/23.
 */

app.filter('subStr', function() {
    return function(text) {
        var newArguments= Array.prototype.slice.call(arguments);
        if (newArguments.length == 1) {
            var length = newArguments[0];
            if (text.length > length) {
                return text.substring(0, length) + '...';
            }
        }
        else if (newArguments.length == 2) {
            var start = newArguments[0];
            var end = newArguments[1];
            if (end < text.length) {
                return text.substring(start, end) + '...';
            }
        }

        return text;
    }
});
