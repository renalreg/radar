(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('anyValue', function(_) {
    return function anyValue(x, callback) {
      var found;
      var value;

      if (_.isArray(x)) {
        for (var i = 0; i < x.length; i++) {
          value = x[i];
          found = anyValue(value, callback);

          if (found) {
            return true;
          }
        }
      } else if (_.isObject(x)) {
        for (var key in x) {
          if (x.hasOwnProperty(key)) {
            value = x[key];
            found = anyValue(value, callback);

            if (found) {
              return true;
            }
          }
        }
      } else {
        return callback(x);
      }
    };
  });
})();
