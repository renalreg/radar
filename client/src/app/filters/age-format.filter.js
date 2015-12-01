(function() {
  'use strict';

  var app = angular.module('radar.filters');

  app.filter('ageFormat', [function() {
    return function ageFormat(seconds) {
      var output;

      if (seconds) {
        var years = seconds / (365 * 24 * 60 * 60);
        var months = Math.floor((years - Math.floor(years)) * 12);
        years = Math.floor(years);

        output = years + ' ' + (years === 1 ? 'year' : 'years') + ', ' + months + ' ' + (months === 1 ? 'month' : 'months');
      } else {
        output = '-';
      }

      return output;
    };
  }]);
})();
