(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudSaveButton', ['$parse', function($parse) {
    return {
      require: ['^crud', '^form', '?^crudSubmit'],
      templateUrl: function(element, attrs) {
        return attrs.action ? 'app/crud/save-button.html' : 'app/crud/save-submit-button.html';
      },
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
          crudSubmitCtrl.on('submitting', function(submitting) {
            scope.submitting = submitting;
          });
        }

        scope.click = function() {
          crudSubmitCtrl.submit(function() {
            return $parse(attrs.action)(scope);
          });
        };
      }
    };
  }]);
})();
