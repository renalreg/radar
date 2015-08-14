(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('fieldError', function() {
    return {
      restrict: 'A',
      transclude: true,
      templateUrl: 'app/forms/field-error.html',
      link: function(scope, element, attrs, ctrl, transclude) {
        transclude(scope, function(clone) {
          element.children().first().append(clone);
        });
      }
    };
  });
})();
