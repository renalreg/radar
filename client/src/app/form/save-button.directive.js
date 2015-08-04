(function() {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrSaveButton', function() {
    return {
      restrict: 'A',
      require: '^form',
      replace: true,
      templateUrl: 'app/form/save-button.html',
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
