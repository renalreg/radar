(function() {
  'use strict';

  var app = angular.module('radar.filters');

  app.filter('genderFormat', function() {
    return function(input) {
      if (input === 'M') {
        return 'Male';
      } else if (input === 'F') {
        return 'Female';
      } else {
        return '-';
      }
    };
  });
})();
