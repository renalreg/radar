(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudSaveButton', function() {
    return {
      require: ['^crud', '^form'],
      scope: {},
      template: '<button ng-disabled="!valid || !enabled" type="submit" class="btn btn-success"><i class="fa fa-floppy-o"></i> Save</button>',
      link: function(scope, element, attrs, ctrls) {
        var crudCtrl = ctrls[0];
        var formCtrl = ctrls[1];

        scope.$watch(function() {
          return formCtrl.$valid;
        }, function(value) {
          scope.valid = value;
        });

        scope.$watch(function() {
          return crudCtrl.saveEnabled();
        }, function(value) {
          scope.enabled = value;
        });
      }
    };
  });
})();
