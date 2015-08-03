(function () {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrFieldHelp', function() {
    return {
      restrict: 'A',
      transclude: true,
      templateUrl: 'app/form/field-help.html',
      link: function(scope, element, attrs, ctrl, transclude) {
        transclude(scope, function(clone) {
          element.children().first().append(clone);
        });
      }
    };
  });
})();
