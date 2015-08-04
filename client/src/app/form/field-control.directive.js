(function() {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrFieldControl', function() {
    return {
      restrict: 'A',
      transclude: true,
      templateUrl: 'app/form/field-control.html',
      link: function(scope, element, attrs, ctrl, transclude) {
        transclude(scope, function(clone) {
          element.children().first().append(clone);
        });
      }
    };
  });
})();
