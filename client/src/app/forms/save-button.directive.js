(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('saveButton', function() {
    return {
      restrict: 'A',
      require: '^form',
      replace: true,
      scope: {
        isSaving: '='
      },
      templateUrl: 'app/forms/save-button.html',
      link: function(scope, element, attrs, formCtrl) {
        scope.canSave = formCtrl.$valid;

        scope.$watch(function() {
          return formCtrl.$valid;
        }, function() {
          scope.canSave = formCtrl.$valid;
        });
      }
    };
  });
})();
