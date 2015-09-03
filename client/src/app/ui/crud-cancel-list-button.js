(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('crudCancelListButton', function() {
    return {
      scope: {},
      template: '<button ng-click="action()" ng-show="enabled" type="button" class="btn btn-link">Cancel</button>',
      link: function(scope) {
        scope.action = function() {
          scope.$parent.list();
        };

        scope.$watch(function() {
          return scope.$parent.listEnabled();
        }, function(value) {
          scope.enabled = value;
        });
      }
    };
  });
})();

