(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('crudCancelViewButton', function() {
    return {
      require: '^form',
      scope: {},
      template: '<button ng-click="action()" ng-show="enabled" type="button" class="btn btn-link">Cancel</button>',
      link: function(scope, element, attrs, formCtrl) {
        scope.action = function() {
          formCtrl.$setPristine(true);
          scope.$parent.view();
        };

        scope.$watch(function() {
          return scope.$parent.viewEnabled();
        }, function(value) {
          scope.enabled = value;
        });
      }
    };
  });
})();
