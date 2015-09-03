(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('crudListRemoveButton', function($timeout) {
    return {
      scope: {
        item: '='
      },
      templateUrl: 'app/ui/crud-list-remove-button.html',
      link: function(scope) {
        scope.clicked = false;
        scope.confirmEnabled = false;

        var confirmTimeout = null;

        scope.remove = function() {
          scope.clicked = true;
          scope.confirmEnabled = false;
          confirmTimeout = $timeout(function() {
            scope.confirmEnabled = true;
          }, 1000);
        };

        scope.confirm = function() {
          scope.clicked = false;
          scope.confirmEnabled = false;
          $timeout.cancel(confirmTimeout);

          scope.$parent.remove(scope.item);
        };

        scope.cancel = function() {
          scope.clicked = false;
          scope.confirmEnabled = false;
          $timeout.cancel(confirmTimeout);
        };

        scope.$watch(function() {
          return scope.$parent.removeEnabled(scope.item);
        }, function(value) {
          scope.removeEnabled = value;
        });

        scope.$watch(function() {
          return scope.$parent.removePermission(scope.item);
        }, function(value) {
          scope.permission = value;
        });
      }
    };
  });
})();
