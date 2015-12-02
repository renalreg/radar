(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudSaveButton', function() {
    return {
      require: ['^crud', '^form', '?^crudSubmit'],
      scope: {},
      templateUrl: 'app/crud/save-button.html',
      link: function(scope, element, attrs, ctrls) {
        var crudCtrl = ctrls[0];
        var formCtrl = ctrls[1];
        var crudSubmitCtrl = ctrls[2];

        scope.submitting = false;

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

        if (crudSubmitCtrl !== null) {
          crudSubmitCtrl.on('submit', function() {
            scope.submitting = true;
          });

          crudSubmitCtrl.on('submitted', function() {
            scope.submitting = false;
          });
        }
      }
    };
  });
})();
