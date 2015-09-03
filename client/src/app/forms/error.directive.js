(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmError', function() {
    return {
      require: '^frmErrors',
      templateUrl: 'app/forms/error.html',
      transclude: true,
      scope: {
        key: '@',
        isDefault: '@'
      },
      link: function(scope, element, attrs, errorsCtrl) {
        var isDefault = scope.isDefault === 'true';

        if (!isDefault) {
          errorsCtrl.override(scope.key);
        }

        scope.showError = function() {
          if (scope.key) {
            return errorsCtrl.showError(scope.key, isDefault);
          } else {
            return true;
          }
        };
      }
    };
  });
})();
