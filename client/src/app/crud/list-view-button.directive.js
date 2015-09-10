(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudListViewButton', function() {
    return {
      require: '^crud',
      scope: {
        item: '='
      },
      template: '<button ng-click="action()" ng-disabled="!enabled" type="button" class="btn btn-xs btn-default"><i class="fa fa-eye"></i> View</button>',
      link: function(scope, element, attrs, crudCtrl) {
        scope.action = function() {
          crudCtrl.view(scope.item);
        };

        scope.$watch(function() {
          return crudCtrl.viewEnabled(scope.item);
        }, function(value) {
          scope.enabled = value;
        });
      }
    };
  });
})();
