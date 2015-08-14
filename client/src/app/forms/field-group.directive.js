(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('fieldGroup', function() {
    return {
      restrict: 'A',
      transclude: true,
      scope: {
        required: '=',
        hasError: '='
      },
      templateUrl: 'app/forms/field-group.html',
      link: function(scope, element, attrs, ctrl, transclude) {
        transclude(scope.$parent, function(clone) {
          element.children().first().append(clone);
        });
      }
    };
  });
})();
