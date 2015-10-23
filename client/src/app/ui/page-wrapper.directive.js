(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('pageWrapper', function() {
    return {
      restrict: 'A',
      transclude: true,
      templateUrl: 'app/ui/page-wrapper.html'
    };
  });
})();
