(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudListEditButton', function() {
    return {
      require: '^crud',
      scope: {
        item: '='
      },
      template: (
          '<button ng-click="action()" ng-if="permission" ng-disabled="!enabled"' +
          ' type="button" class="btn btn-xs btn-primary">' +
          '<i class="fa fa-pencil"></i> Edit' +
          '</button>'
      ),
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
      }
    };
  });
})();
