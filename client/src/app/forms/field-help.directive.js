(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('fieldHelp', function() {
    return {
      restrict: 'A',
      transclude: true,
      templateUrl: 'app/forms/field-help.html',
      link: function(scope, element, attrs, ctrl, transclude) {
        transclude(scope, function(clone) {
          element.children().first().append(clone);
        });
      }
    };
  });
})();
