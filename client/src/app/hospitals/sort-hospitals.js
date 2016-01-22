(function() {
  'use strict';

  var app = angular.module('radar.hospitals');

  app.factory('sortHospitals', ['_', function(_) {
    return function sortHospitals(hospitals) {
      return _.sortBy(hospitals, function(x) {
        return x.name.toUpperCase();
      });
    };
  }]);
})();
