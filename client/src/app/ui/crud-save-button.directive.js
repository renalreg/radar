(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('crudSaveButton', function() {
    return {
      require: '^form',
      scope: {},
      template: '<button ng-disabled="formCtrl.$invalid || !enabled" type="submit" class="btn btn-success"><i class="fa fa-floppy-o"></i> Save</button>',
      link: function(scope, element, attrs, formCtrl) {
        console.log(formCtrl);
        scope.formCtrl = formCtrl;

        scope.$watch(function() {
          return scope.$parent.saveEnabled();
        }, function(value) {
          scope.enabled = value;
        });
      }
    };
  });
})();
