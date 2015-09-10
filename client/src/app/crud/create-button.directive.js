(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudCreateButton', function() {
    return {
      require: '^crud',
      scope: {
        action: '&'
      },
      template: '<button ng-click="action()" ng-if="permission" ng-disabled="!enabled" type="button" class="btn btn-primary">New</button>',
      link: function(scope, element, attrs, crudCtrl) {
        scope.$watch(function() {
          return crudCtrl.createEnabled(scope.item);
        }, function(value) {
          scope.enabled = value;
        });

        scope.$watch(function() {
          return crudCtrl.createPermission(scope.item);
        }, function(value) {
          scope.permission = value;
        });
      }
    };
  });
})();
