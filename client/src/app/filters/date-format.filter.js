(function() {
  'use strict';

  var app = angular.module('radar.filters');

  app.filter('dateFormat', function(moment) {
    return function(input) {
      if (input) {
        return moment(input, 'YYYY-MM-DD').format('DD/MM/YYYY');
      } else {
        return '';
      }
    };
  });
})();
