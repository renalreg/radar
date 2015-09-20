(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmGroup', function() {
    return {
      require: 'frmField',
      transclude: true,
      templateUrl: 'app/forms/group.html',
      scope: {},
      link: function(scope, element, attrs, fieldCtrl) {
        scope.isValid = function() {
          return fieldCtrl.isValid();
        };

        scope.isRequired = function() {
          return fieldCtrl.isRequired();
        };
      }
    };
  });
})();
