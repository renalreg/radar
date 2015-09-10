(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudCancelButton', function() {
    return {
      require: ['^crud', '^form'],
      scope: {
        action: '&'
      },
      template: '<button ng-click="click()" ng-disabled="!enabled" type="button" class="btn btn-link">Cancel</button>',
      link: function(scope, element, attrs, ctrls) {
        var crudCtrl = ctrls[0];
        var formCtrl = ctrls[1];

        scope.click = function() {
          formCtrl.$setPristine(true);
          scope.action();
        };

        scope.$watch(function() {
          return crudCtrl.cancelEnabled();
        }, function(value) {
          scope.enabled = value;
        });
      }
    };
  });
})();
