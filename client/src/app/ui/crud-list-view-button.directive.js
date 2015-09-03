(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('crudListViewButton', function() {
    return {
      scope: {
        item: '='
      },
      template: '<button ng-click="action()" ng-disabled="!enabled" type="button" class="btn btn-xs btn-default"><i class="fa fa-eye"></i> View</button>',
      link: function(scope) {
        scope.action = function() {
          scope.$parent.view(scope.item);
        };

        scope.$watch(function() {
          return scope.$parent.viewEnabled(scope.item);
        }, function(value) {
          scope.enabled = value;
        });
      }
    };
  });
})();
