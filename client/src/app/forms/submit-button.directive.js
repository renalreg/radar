(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('submitButton', function() {
    return {
      require: ['^form', '?^submitIfValid'],
      scope: {},
      transclude: true,
      template: '<button ng-disabled="formCtrl.$invalid" type="submit" class="btn btn-success"><span ng-transclude></span> <i class="fa fa-spinner fa-spin" ng-show="submitting"></i></button>',
      link: function(scope, element, attrs, ctrls) {
        var formCtrl = ctrls[0];
        var submitIfValidCtrl = ctrls[1];

        scope.formCtrl = formCtrl;
        scope.submitting = false;

        if (submitIfValidCtrl !== null) {
          submitIfValidCtrl.on('submit', function() {
            scope.submitting = true;
          });

          submitIfValidCtrl.on('done', function() {
            scope.submitting = false;
          });
        }
      }
    };
  });
})();
