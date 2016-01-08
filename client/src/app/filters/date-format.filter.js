(function() {
  'use strict';

  var app = angular.module('radar.filters');

  app.filter('dateFormat', function() {
    return function(oldValue) {
      var newValue;

      if (oldValue) {
        var year = oldValue.substr(0, 4);
        var month = oldValue.substr(5, 2);
        var day = oldValue.substr(8, 2);

        newValue = day + '/' + month + '/' + year;
      } else {
        newValue = '-';
      }

      return newValue;
    };
  });
})();
