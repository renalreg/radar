(function () {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrFieldLabel', function() {
    return {
      restrict: 'A',
      transclude: true,
      templateUrl: 'app/form/field-label.html',
      link: function(scope, element, attrs, ctrl, transclude) {
        transclude(scope, function(clone) {
          element.children().first().append(clone);
        });
      }
    };
  });
})();
