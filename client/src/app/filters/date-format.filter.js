(function() {
  'use strict';

  var app = angular.module('radar.filters');

  app.filter('dateFormat', function(moment) {
    return function(input) {
      if (input) {
        var date = moment(input, 'YYYY-MM-DD');

        if (date.isValid()) {
          return date.format('DD/MM/YYYY');
        } else {
          return '-';
        }
      } else {
        return '-';
      }
    };
  });
})();
