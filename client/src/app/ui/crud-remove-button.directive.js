(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('crudRemoveButton', function() {
    return {
      scope: {
        item: '='
      },
      template: '<button ng-click="action()" ng-if="permission" ng-disabled="!enabled" type="button" class="btn btn-link"><i class="fa fa-trash-o"></i> Delete</button>',
      link: function(scope) {
        scope.action = function() {
          scope.$parent.remove(scope.item);
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
