(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudCancelListButton', function() {
    return {
      require: ['^crud', '^form'],
      scope: {},
      template: '<button ng-click="action()" ng-show="enabled" type="button" class="btn btn-link">Cancel</button>',
      link: function(scope, element, attrs, ctrls) {
        var crudCtrl = ctrls[0];
        var formCtrl = ctrls[1];

        scope.action = function() {
          formCtrl.$setPristine(true);
          crudCtrl.list();
        };

        scope.$watch(function() {
          return crudCtrl.listEnabled();
        }, function(value) {
          scope.enabled = value;
        });
      }
    };
  });
})();

