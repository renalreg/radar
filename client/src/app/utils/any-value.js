(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('anyValue', ['_', function(_) {
    return function anyValue(x, callback) {
      var found = false;
      var value;

      if (_.isArray(x)) {
        for (var i = 0; i < x.length; i++) {
          value = x[i];
          found = anyValue(value, callback);

          if (found) {
            break;
          }
        }
      } else if (_.isObject(x)) {
        for (var key in x) {
          if (x.hasOwnProperty(key)) {
            value = x[key];
            found = anyValue(value, callback);

            if (found) {
              break;
            }
          }
        }
      } else {
        found = callback(x);
      }

      return found;
    };
  }]);
})();
