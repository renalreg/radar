(function() {
  'use strict';

  var app = angular.module('radar.validators');

  var NUMBER_REGEX = /^[+-]?[0-9]+(\.[0-9]+)?$/;

  // TODO
  app.directive('numberValidator', function() {
    return {
      restrict: 'A'
    };
  });
})();
