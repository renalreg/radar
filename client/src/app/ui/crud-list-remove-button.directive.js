(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('crudListRemoveButton', function() {
    return {
      scope: {
        item: '='
      },
      templateUrl: 'app/ui/crud-list-remove-button.html',
      link: function(scope) {
        scope.clicked = false;

        scope.delete = function() {
          scope.clicked = true;
        };

        scope.confirm = function() {
          scope.clicked = false;
          scope.$parent.remove(scope.item);
        };

        scope.cancel = function() {
          scope.clicked = false;
        };

        scope.$watch(function() {
          return scope.$parent.removeEnabled(scope.item);
        }, function(value) {
          scope.enabled = value;
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
