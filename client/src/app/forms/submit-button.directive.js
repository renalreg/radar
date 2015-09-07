(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('submitButton', function() {
    return {
      require: '^form',
      scope: {},
      transclude: true,
      template: '<button ng-disabled="formCtrl.$invalid" type="submit" class="btn btn-success" ng-transclude></button>',
      link: function(scope, element, attrs, formCtrl) {
        scope.formCtrl = formCtrl;
      }
    };
  });
})();
