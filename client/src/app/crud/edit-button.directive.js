(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudEditButton', function() {
    return {
      require: '^crud',
      scope: {
        item: '='
      },
      template: '<button ng-click="action()" ng-if="permission && visible" ng-disabled="!enabled" type="button" class="btn btn-primary">Edit</button>',
      link: function(scope, element, attrs, crudCtrl) {
        scope.action = function() {
          crudCtrl.edit(scope.item);
        };

        scope.$watch(function() {
          return crudCtrl.editEnabled(scope.item);
        }, function(value) {
          scope.enabled = value;
        });

        scope.$watch(function() {
          return crudCtrl.editPermission(scope.item);
        }, function(value) {
          scope.permission = value;
        });

        scope.$watch(function() {
          return crudCtrl.editVisible(scope.item);
        }, function(value) {
          scope.visible = value;
        });
      }
    };
  });
})();
