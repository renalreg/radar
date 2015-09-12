(function() {
  'use strict';

  var app = angular.module('radar.filters');

  app.filter('dateTimeFormat', function(moment) {
    return function(input) {
      if (input) {
        var dt = moment(input);

        if (dt.isValid()) {
          return dt.format('DD/MM/YYYY HH:MM:SS');
        } else {
          return '-';
        }
      } else {
        return '-';
      }
    };
  });
})();
