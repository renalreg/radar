(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('getValueAtPath', function() {
    return function getValueAtPath(o, path) {
      var paths = path.split('.');

      for (var i = 0; i < paths.length; i++) {
        o = o[paths[i]];

        if (o === undefined) {
          break;
        }
      }

      return o;
    };
  });
})();
