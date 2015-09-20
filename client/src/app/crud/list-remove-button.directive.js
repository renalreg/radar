(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudListRemoveButton', ['$timeout', function($timeout) {
    return {
      require: '^crud',
      scope: {
        item: '='
      },
      templateUrl: 'app/crud/list-remove-button.html',
      link: function(scope, element, attrs, crudCtrl) {
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
          crudCtrl.remove(scope.item);
        };

        scope.cancel = function() {
          scope.clicked = false;
          scope.confirmEnabled = false;
          $timeout.cancel(confirmTimeout);
        };

        scope.$watch(function() {
          return crudCtrl.removeEnabled(scope.item);
        }, function(value) {
          scope.removeEnabled = value;
        });

        scope.$watch(function() {
          return crudCtrl.removePermission(scope.item);
        }, function(value) {
          scope.permission = value;
        });
      }
    };
  }]);
})();
