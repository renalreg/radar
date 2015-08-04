(function() {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrCancelButton', function($window) {
    return {
      restrict: 'A',
      require: '^form',
      replace: true,
      scope: {
        modified: '&',
        action: '&'
      },
      templateUrl: 'app/form/cancel-button.html',
      link: function(scope, element) {
        element.on('click', function() {
          if (scope.modified()) {
            if ($window.confirm('Discard changes?')) {
              scope.$apply(function() {
                scope.action();
              });
            }
          } else {
            scope.$apply(function() {
              scope.action();
            });
          }
        });
      }
    };
  });
})();

