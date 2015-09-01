(function() {
  'use strict';

  var app = angular.module('radar.filters');

  app.filter('missing', function() {
    return function(input) {
      if (input === '' || input === null || input === undefined) {
        return '-';
      } else {
        return input;
      }
    };
  });
})();

