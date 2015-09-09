(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('crudCreateButton', function() {
    return {
      scope: {
        action: '&'
      },
      template: '<button ng-click="action()" ng-if="permission" ng-disabled="!enabled" type="button" class="btn btn-primary">New</button>',
      link: function(scope) {
        scope.$watch(function() {
          return scope.$parent.createEnabled(scope.item);
        }, function(value) {
          scope.enabled = value;
        });

        scope.$watch(function() {
          return scope.$parent.createPermission(scope.item);
        }, function(value) {
          scope.permission = value;
        });
      }
    };
  });
})();
