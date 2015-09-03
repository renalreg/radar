(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('crudListButton', function() {
    return {
      scope: {},
      template: '<button ng-click="action()" ng-disabled="!enabled" type="button" class="btn btn-default">List</button>',
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
