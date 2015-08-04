(function() {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrFieldGroup', function() {
    return {
      restrict: 'A',
      transclude: true,
      scope: {
        required: '=',
        hasError: '='
      },
      templateUrl: 'app/form/field-group.html',
      link: function(scope, element, attrs, ctrl, transclude) {
        transclude(scope.$parent, function(clone) {
          element.children().first().append(clone);
        });
      }
    };
  });
})();
