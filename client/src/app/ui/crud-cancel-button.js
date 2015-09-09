(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('crudCancelButton', function() {
    return {
      require: '^form',
      scope: {
        action: '&'
      },
      template: '<button ng-click="click()" ng-disabled="!enabled" type="button" class="btn btn-link">Cancel</button>',
      link: function(scope, element, attrs, formCtrl) {
        scope.click = function() {
          formCtrl.$setPristine(true);
          scope.action();
        };

        scope.$watch(function() {
          return scope.$parent.cancelEnabled();
        }, function(value) {
          scope.enabled = value;
        });
      }
    };
  });
})();
